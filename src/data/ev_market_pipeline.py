"""Ingest and analyze a real Indian EV registration export.

The module is fail-closed: it never creates a dataset when no source export exists,
and it does not turn invalid rows into valid observations. Place an official or
otherwise documented public CSV/XLSX export in data/raw/ev_market/ before running.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from analytics.market_analysis import (
    REGION_MAP,
    category_analysis,
    category_year_growth,
    cagr_value,
    manufacturer_analysis,
    regional_analysis,
    state_analysis,
    state_year_growth,
    yearly_market_growth,
)

RAW_DIR = ROOT / "data" / "raw" / "ev_market"
PROCESSED_DIR = ROOT / "data" / "processed" / "ev_market"
OUTPUT_DIR = ROOT / "outputs" / "market"

STATE_ALIASES = {
    "ORISSA": "Odisha", "PONDICHERRY": "Puducherry", "UTTARANCHAL": "Uttarakhand",
    "NCT OF DELHI": "Delhi", "DADRA & NAGAR HAVELI": "Dadra and Nagar Haveli and Daman and Diu",
    "DADRA AND NAGAR HAVELI": "Dadra and Nagar Haveli and Daman and Diu",
    "THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU": "Dadra and Nagar Haveli and Daman and Diu",
}
STATE_NAMES = set(REGION_MAP)
CATEGORY_ALIASES = {
    "2 WHEELER": "2W", "TWO WHEELER": "2W", "TWO-WHEELER": "2W", "2W": "2W",
    "MOTORCYCLE": "2W", "SCOOTER": "2W", "ELECTRIC TWO WHEELER": "2W",
}
FUEL_ALIASES = {
    "ELECTRIC(BOV)": "ELECTRIC", "ELECTRIC (BOV)": "ELECTRIC", "PURE EV": "ELECTRIC", "EV": "ELECTRIC",
}
MANUFACTURER_ALIASES = {
    "OLA ELECTRIC": "Ola Electric", "TVS MOTOR": "TVS Motor Company", "BAJAJ AUTO": "Bajaj Auto",
    "ATHER ENERGY": "Ather Energy", "HERO ELECTRIC": "Hero Electric", "HERO MOTOCORP": "Hero MotoCorp",
}
COLUMN_ALIASES = {
    "date": "date", "month": "date", "year": "year", "financial year": "year",
    "state": "state", "state name": "state", "state/ut": "state", "ut": "state",
    "vehicle category": "vehicle_category", "vehicle type": "vehicle_category", "category": "vehicle_category",
    "manufacturer": "manufacturer", "maker": "manufacturer", "oem": "manufacturer",
    "fuel type": "fuel_type", "fuel": "fuel_type", "fuel category": "fuel_type",
    "registration count": "registrations", "registrations": "registrations", "count": "registrations",
    "ev registrations": "registrations", "e2w registrations": "registrations",
}


def normalize_column_name(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).strip().lower()).strip()


def normalize_state(value: object) -> str | pd.NA:
    if pd.isna(value):
        return pd.NA
    clean = re.sub(r"\s+", " ", str(value).strip()).upper()
    if clean in STATE_ALIASES:
        return STATE_ALIASES[clean]
    for state in STATE_NAMES:
        if clean == state.upper():
            return state
    return str(value).strip().title()


def normalize_category(value: object) -> str | pd.NA:
    if pd.isna(value):
        return pd.NA
    clean = re.sub(r"\s+", " ", str(value).strip()).upper()
    return CATEGORY_ALIASES.get(clean, str(value).strip())


def normalize_fuel(value: object) -> str | pd.NA:
    if pd.isna(value):
        return pd.NA
    clean = re.sub(r"\s+", " ", str(value).strip()).upper()
    return FUEL_ALIASES.get(clean, str(value).strip().upper())


def normalize_manufacturer(value: object) -> str | pd.NA:
    if pd.isna(value):
        return pd.NA
    clean = re.sub(r"\s+", " ", str(value).strip()).upper()
    return MANUFACTURER_ALIASES.get(clean, str(value).strip())


def _read_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, dtype=object)
    return pd.read_excel(path, dtype=object)


def _find_inputs(input_path: str | None) -> list[Path]:
    if input_path:
        path = Path(input_path)
        if not path.is_absolute():
            path = ROOT / path
        return [path] if path.exists() else []
    return sorted(path for path in RAW_DIR.iterdir() if path.suffix.lower() in {".csv", ".xlsx", ".xls"} and not path.name.startswith("~")) if RAW_DIR.exists() else []


def normalize_frame(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    renamed = {}
    for column in frame.columns:
        key = normalize_column_name(column)
        renamed[column] = COLUMN_ALIASES.get(key, key.replace(" ", "_"))
    frame = frame.rename(columns=renamed).copy()
    issues: list[dict] = []
    required = ["state", "registrations"]
    missing = [column for column in required if column not in frame.columns]
    if "year" not in frame.columns and "date" not in frame.columns:
        missing.append("year or date")
    if missing:
        raise ValueError(f"Missing required columns: {missing}; expected year or date, state, registrations")
    if "year" not in frame.columns:
        frame["year"] = pd.NA
    if "date" in frame.columns:
        source_dates = frame["date"].copy()
        dates = pd.to_datetime(source_dates, errors="coerce")
        frame["_invalid_date"] = dates.isna() & source_dates.notna()
        frame["date"] = dates.dt.date
        derived_year = dates.dt.year
        if frame["year"].notna().any():
            supplied_year = pd.to_numeric(frame["year"], errors="coerce")
            mismatch = supplied_year.notna() & derived_year.notna() & (supplied_year != derived_year)
            if mismatch.any():
                issues.append({"status": "ERROR", "check": "year_date_mismatch", "rows": mismatch[mismatch].index.tolist()})
        frame["year"] = frame["year"].where(frame["year"].notna(), derived_year)
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame["state"] = frame["state"].map(normalize_state)
    frame["registrations_raw"] = frame["registrations"]
    frame["registrations"] = pd.to_numeric(frame["registrations"], errors="coerce")
    if "vehicle_category" in frame.columns:
        frame["vehicle_category"] = frame["vehicle_category"].map(normalize_category)
        source_category = frame["vehicle_category"].astype("string").str.upper()
        frame["source_category"] = frame["vehicle_category"]
        frame.loc[source_category.eq("FUEL"), "vehicle_category"] = pd.NA
    if "fuel_type" in frame.columns:
        frame["fuel_type"] = frame["fuel_type"].map(normalize_fuel)
    if "manufacturer" in frame.columns:
        frame["manufacturer"] = frame["manufacturer"].map(normalize_manufacturer)
    return frame, issues


def validate_frame(frame: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    errors: list[dict] = []
    warnings: list[dict] = []
    checks: list[dict] = []
    def check(name: str, status: str, detail: str, rows: list[int] | None = None) -> None:
        item = {"check": name, "status": status, "detail": detail}
        if rows:
            item["rows"] = rows
        checks.append(item)
        (errors if status == "ERROR" else warnings if status == "WARNING" else []).append(item)

    missing_year = frame["year"].isna()
    check("missing_year", "ERROR" if missing_year.any() else "VALID", f"{int(missing_year.sum())} rows missing year", frame.index[missing_year].tolist())
    invalid_year = frame["year"].notna() & ~frame["year"].between(1900, datetime.now().year + 1)
    check("invalid_year", "ERROR" if invalid_year.any() else "VALID", f"{int(invalid_year.sum())} rows outside supported year bounds", frame.index[invalid_year].tolist())
    invalid_date = frame.get("_invalid_date", pd.Series(False, index=frame.index))
    check("invalid_date", "ERROR" if invalid_date.any() else "VALID", f"{int(invalid_date.sum())} rows with an unparseable date", frame.index[invalid_date].tolist())
    missing_state = frame["state"].isna() | frame["state"].astype("string").str.strip().eq("")
    check("missing_state", "ERROR" if missing_state.any() else "VALID", f"{int(missing_state.sum())} rows missing state", frame.index[missing_state].tolist())
    unknown_state = frame["state"].notna() & ~frame["state"].isin(STATE_NAMES)
    check("unknown_state", "ERROR" if unknown_state.any() else "VALID", f"{int(unknown_state.sum())} rows with unknown state", frame.index[unknown_state].tolist())
    non_numeric = frame["registrations"].isna() & frame["registrations_raw"].notna()
    check("non_numeric_registrations", "ERROR" if non_numeric.any() else "VALID", f"{int(non_numeric.sum())} non-numeric registration values", frame.index[non_numeric].tolist())
    negative = frame["registrations"].notna() & (frame["registrations"] < 0)
    check("negative_registrations", "ERROR" if negative.any() else "VALID", f"{int(negative.sum())} negative registration values", frame.index[negative].tolist())
    exact_dupes = frame.duplicated(keep=False)
    check("duplicate_records", "ERROR" if exact_dupes.any() else "VALID", f"{int(exact_dupes.sum())} rows in exact duplicate groups", frame.index[exact_dupes].tolist())
    key_columns = [column for column in ["year", "state", "vehicle_category", "fuel_type", "manufacturer"] if column in frame]
    key_dupes = frame.duplicated(key_columns, keep=False) if key_columns else pd.Series(False, index=frame.index)
    check("duplicate_aggregation_keys", "WARNING" if key_dupes.any() else "VALID", f"{int(key_dupes.sum())} rows share an aggregation key; rows are retained and summed", frame.index[key_dupes].tolist())
    for column, label in [("vehicle_category", "unexpected_vehicle_category"), ("fuel_type", "unexpected_fuel_type")]:
        if column in frame:
            missing = frame[column].isna()
            check(f"missing_{column}", "WARNING" if missing.any() else "VALID", f"{int(missing.sum())} rows missing {column}")
            unexpected = frame[column].notna() & ~frame[column].isin({"2W", "ELECTRIC"} if column == "vehicle_category" else {"ELECTRIC"})
            check(label, "WARNING" if unexpected.any() else "VALID", f"{int(unexpected.sum())} rows have values outside the expected vocabulary")
        else:
            check(f"missing_{column}", "WARNING", f"{column} column is not available in source")
    if "manufacturer" not in frame:
        check("missing_manufacturer", "WARNING", "manufacturer column is not available in source")
    else:
        missing = frame["manufacturer"].isna() | frame["manufacturer"].eq("")
        check("missing_manufacturer", "WARNING" if missing.any() else "VALID", f"{int(missing.sum())} rows missing manufacturer")
    valid = ~missing_year & ~invalid_year & ~invalid_date & ~missing_state & ~unknown_state & ~non_numeric & ~negative
    return {"status": "ERROR" if errors else "WARNING" if warnings else "VALID", "checks": checks, "error_count": len(errors), "warning_count": len(warnings)}, frame.loc[~valid].copy()


def write_summary(df: pd.DataFrame, report: dict) -> None:
    yearly = yearly_market_growth(df)
    state = state_analysis(df)
    manufacturer = manufacturer_analysis(df)
    category = category_analysis(df)
    regional = regional_analysis(df)
    yearly.to_csv(OUTPUT_DIR / "yearly_market_growth.csv", index=False)
    state.to_csv(OUTPUT_DIR / "state_analysis.csv", index=False)
    state_year_growth(df).to_csv(OUTPUT_DIR / "state_year_growth.csv", index=False)
    manufacturer.to_csv(OUTPUT_DIR / "manufacturer_analysis.csv", index=False)
    category.to_csv(OUTPUT_DIR / "category_analysis.csv", index=False)
    category_year_growth(df).to_csv(OUTPUT_DIR / "category_year_growth.csv", index=False)
    regional.to_csv(OUTPUT_DIR / "regional_analysis.csv", index=False)
    years = sorted(df["year"].astype(int).unique())
    states = sorted(df["state"].unique())
    kpis = pd.DataFrame([{
        "actual_years": len(years), "actual_states": len(states), "period_start": years[0], "period_end": years[-1],
        "total_registrations": df["registrations"].sum(), "cagr_pct": cagr_value(df),
        "supports_10_plus_years": len(years) >= 10, "supports_20_plus_states": len(states) >= 20,
        "adoption_rate_available": "total_vehicle_registrations" in df.columns,
    }])
    kpis.to_csv(OUTPUT_DIR / "market_kpis.csv", index=False)
    def markdown_table(table: pd.DataFrame) -> str:
        if table.empty:
            return "No data was available."
        columns = list(table.columns)
        rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
        rows.extend("| " + " | ".join(str(value) for value in row) + " |" for row in table.astype(object).itertuples(index=False, name=None))
        return "\n".join(rows)

    lines = ["# EV Market Analysis Summary", "", f"Actual year coverage: {len(years)} years", f"Actual state coverage: {len(states)} states", f"Actual dataset period: {years[0]}–{years[-1]}", f"Total registrations: {df['registrations'].sum():,.0f}", f"CAGR (%): {cagr_value(df) if cagr_value(df) is not None else 'Not valid for this data'}", "", f"Supports 10+ years: {'YES' if len(years) >= 10 else 'NO'}", f"Supports 20+ states: {'YES' if len(states) >= 20 else 'NO'}", "Adoption rate supported: NO unless a total vehicle-registration denominator is present.", "", "## Top states", markdown_table(state.head(10)), "", "## Manufacturers", markdown_table(manufacturer.head(10)), "", "## Categories", markdown_table(category), "", "## Regions", markdown_table(regional), "", "Only observed rows in the supplied source were analyzed; no missing historical values were filled."]
    (OUTPUT_DIR / "market_analysis_summary.md").write_text("\n".join(lines), encoding="utf-8")


def run(input_path: str | None = None, fuel_type: str | None = "ELECTRIC") -> dict:
    inputs = _find_inputs(input_path)
    if not inputs:
        raise FileNotFoundError("No CSV/XLSX source export found in data/raw/ev_market/. Follow data/raw/ev_market/README.md and place the unedited public export there.")
    frames, source_files = [], []
    source_rows = 0
    for path in inputs:
        frame = _read_file(path)
        source_rows += len(frame)
        normalized, pre_issues = normalize_frame(frame)
        if fuel_type is not None:
            if "fuel_type" not in normalized.columns:
                raise ValueError("The selected EV analysis requires a fuel_type column; no fuel filter was applied.")
            normalized = normalized[normalized["fuel_type"].eq(fuel_type)].copy()
        normalized["source_file"] = path.name
        frames.append(normalized)
        source_files.append(path.name)
    combined = pd.concat(frames, ignore_index=True)
    validation, rejected = validate_frame(combined)
    validation.update({"generated_at_utc": datetime.now(timezone.utc).isoformat(), "source_files": source_files, "fuel_filter": fuel_type, "rows_read": source_rows, "rows_after_filter": len(combined), "rows_accepted": len(combined) - len(rejected), "rows_rejected": len(rejected), "year_coverage": sorted(combined["year"].dropna().astype(int).unique().tolist()), "state_coverage": sorted(combined["state"].dropna().unique().tolist())})
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / "validation_report.json").write_text(json.dumps(validation, indent=2, default=str), encoding="utf-8")
    rejected.to_csv(PROCESSED_DIR / "rejected_records.csv", index=False)
    if validation["status"] == "ERROR":
        raise ValueError(f"Market source failed validation with {validation['error_count']} error checks. See {PROCESSED_DIR / 'validation_report.json'} and rejected_records.csv.")
    clean = combined.drop(columns=["registrations_raw", "_invalid_date"], errors="ignore")
    clean.to_csv(PROCESSED_DIR / "ev_market_cleaned.csv", index=False)
    write_summary(clean, validation)
    return validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="CSV/XLSX path, relative to the repository root or absolute")
    parser.add_argument("--fuel-type", default="ELECTRIC", help="Normalized fuel value to analyze; use NONE to disable filtering")
    args = parser.parse_args()
    fuel_type = None if args.fuel_type.upper() == "NONE" else args.fuel_type.upper()
    try:
        report = run(args.input, fuel_type=fuel_type)
    except FileNotFoundError as exc:
        print(json.dumps({"status": "NO_SOURCE", "message": str(exc)}, indent=2))
        return 2
    print(json.dumps({"status": report["status"], "actual_years": len(report["year_coverage"]), "actual_states": len(report["state_coverage"]), "period": [report["year_coverage"][0], report["year_coverage"][-1]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
