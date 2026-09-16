import pandas as pd
import pytest

from analytics.market_analysis import cagr_value, manufacturer_analysis, state_analysis, yearly_market_growth
from data.ev_market_pipeline import normalize_category, normalize_state, validate_frame


def sample_frame():
    return pd.DataFrame({
        "year": [2020, 2021, 2020],
        "state": ["Karnataka", "Karnataka", "Maharashtra"],
        "vehicle_category": ["TWO WHEELER", "2W", "2W"],
        "fuel_type": ["ELECTRIC(BOV)", "ELECTRIC", "ELECTRIC"],
        "manufacturer": ["OLA ELECTRIC", "Ola Electric", "TVS MOTOR"],
        "registrations": [100, 150, 50],
    })


def test_year_and_state_normalization():
    assert normalize_state("Orissa") == "Odisha"
    assert normalize_state("NCT of Delhi") == "Delhi"
    assert normalize_category("two wheeler") == "2W"


def test_numeric_conversion_and_duplicate_detection():
    frame = sample_frame()
    frame["registrations_raw"] = frame["registrations"]
    frame["registrations"] = pd.to_numeric(frame["registrations"], errors="coerce")
    report, rejected = validate_frame(frame)
    assert report["status"] == "VALID"
    assert rejected.empty

    duplicate = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    report, rejected = validate_frame(duplicate)
    assert report["status"] == "ERROR"
    assert any(check["check"] == "duplicate_records" for check in report["checks"])


def test_yoy_and_cagr_calculation():
    frame = sample_frame()
    yearly = yearly_market_growth(frame)
    assert yearly.loc[yearly["year"] == 2020, "total_registrations"].item() == 150
    assert yearly.loc[yearly["year"] == 2021, "yoy_growth_pct"].item() == pytest.approx(0)
    assert cagr_value(frame) == pytest.approx(0)


def test_market_share_and_state_aggregation():
    frame = sample_frame()
    states = state_analysis(frame)
    manufacturers = manufacturer_analysis(frame)
    assert states.iloc[0]["state"] == "Karnataka"
    assert states.iloc[0]["share_of_total_pct"] == pytest.approx(50)
    assert manufacturers.iloc[0]["market_share_pct"] == pytest.approx(83.333333, rel=1e-5)
