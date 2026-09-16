# EV Market Raw Data

## Dataset

The acquired raw file is `tdc_vahan_vehicle_registrations_by_fuel_type.csv`.

- Dataset/resource name: Vahan Vehicle Registrations - India, registrations by fuel type
- Publisher/distributor: Transport Data Commons CKAN portal
- Classification: **DERIVED FROM OFFICIAL DATA**; the distributor identifies Vahan/Parivahan as the original source
- Original publisher: Ministry of Road Transport & Highways / Parivahan Vahan
- Original source: https://vahan.parivahan.gov.in/vahan4dashboard/
- Public resource URL: https://ckan.tdc.prod.datopian.com/dataset/111bf9f0-7268-4c27-ab58-29701b18a33a/resource/9597f1c6-0500-4558-bc90-105a95a3619a/download/vahan-vehicle-registrations-by-fuel-type-nmiqeb.csv
- Download date: 2026-09-16
- File coverage observed: 2019-2024
- Geographic coverage observed: 34 states/UTs with accepted EV rows
- Raw records: 418,372 across all fuel types
- EV records selected: 56,767 (`Electric(Bov)` and `Pure Ev`)
- EV registration total selected: 17,572,522
- Manufacturer coverage: not available in this resource
- Vehicle-category coverage: not available; source `category=Fuel` is not a vehicle class
- License/usage: no explicit license was exposed in the downloaded resource metadata; verify terms before redistribution

## Source and provenance

- Preferred publisher: Ministry of Road Transport & Highways, Parivahan/Vahan
- Vahan dashboard: https://vahan.parivahan.gov.in/vahan4dashboard/
- Analytics dashboard: https://analytics.parivahan.gov.in/analytics/publicdashboard/vahan
- OGD portal: https://data.gov.in/
- Source status: downloaded public CKAN resource; the raw file is retained unchanged
- Official/derived status: derived from an official Vahan source, not a direct official Vahan export

## Manual acquisition

1. Open the official dashboard in a normal browser session.
2. Select the report that exposes vehicle category/fuel, state, maker, and date/year fields.
3. Filter for the required EV category and export CSV/XLSX using the portal's own export control.
4. Do not bypass CAPTCHA, authentication, rate limits, or other access controls.
5. Keep the original export unchanged and place it in this directory.
6. Record the filename, source URL, publisher, download date, coverage, license/usage terms, and SHA-256 hash in `DATA_MANIFEST.md`.
7. Run from the repository root:

```text
python src/data/ev_market_pipeline.py
```

Use a specific file when several exports are present:

```text
python src/data/ev_market_pipeline.py --input data/raw/ev_market/source_export.xlsx
```

## Expected fields

The pipeline accepts common aliases for:

- year or date/month
- state
- registration count
- vehicle category/type (optional but recommended)
- manufacturer/maker (optional but recommended)
- fuel type (optional but recommended)

The actual source coverage, not a target, is reported by the pipeline. It will not create missing years, states, registrations, or denominators. The current run filters only `Electric(Bov)` and `Pure Ev`; hybrid fuel labels are excluded.
