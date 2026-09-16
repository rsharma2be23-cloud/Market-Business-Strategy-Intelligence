# EV Market Data Acquisition Report

## 1. Dataset selected

Selected resource: **Vahan Vehicle Registrations - India, by fuel type**.

Raw file: [data/raw/ev_market/tdc_vahan_vehicle_registrations_by_fuel_type.csv](../data/raw/ev_market/tdc_vahan_vehicle_registrations_by_fuel_type.csv)

## 2. Why it was selected

It is directly downloadable from a public CKAN endpoint, contains dated state-level registration rows and fuel labels, and identifies Vahan/Parivahan as the original source. It is stronger than the repository's previous generated proxy data, while still being labeled **derived from official data** rather than an official direct export.

## 3. Original source and acquisition

- Original publisher: Ministry of Road Transport & Highways / Parivahan Vahan
- Original source: https://vahan.parivahan.gov.in/vahan4dashboard/
- Distributor page: https://portal.transport-data.org/@vahan/vahan-vehicle-registrations-india
- Direct public resource: https://ckan.tdc.prod.datopian.com/dataset/111bf9f0-7268-4c27-ab58-29701b18a33a/resource/9597f1c6-0500-4558-bc90-105a95a3619a/download/vahan-vehicle-registrations-by-fuel-type-nmiqeb.csv
- Acquisition date: 2026-09-16
- Acquisition method: ordinary public HTTPS download; no login, API key, CAPTCHA bypass, or restricted access was used
- License: no explicit license was exposed in the downloaded resource metadata; usage and redistribution terms require verification before republishing

## 4. Coverage

- Date range in the downloaded file: 2019-2024
- Years covered: 6
- States/UTs with accepted EV rows: 34
- State names: Andaman and Nicobar Islands; Andhra Pradesh; Arunachal Pradesh; Assam; Bihar; Chandigarh; Chhattisgarh; Dadra and Nagar Haveli and Daman and Diu; Delhi; Goa; Gujarat; Haryana; Himachal Pradesh; Jammu and Kashmir; Jharkhand; Karnataka; Kerala; Ladakh; Madhya Pradesh; Maharashtra; Manipur; Meghalaya; Mizoram; Nagaland; Odisha; Puducherry; Punjab; Rajasthan; Sikkim; Tamil Nadu; Tripura; Uttar Pradesh; Uttarakhand; West Bengal
- Vehicle coverage: not disaggregated by vehicle class in this resource; source `category` is `Fuel`
- Manufacturer coverage: unavailable in this resource
- Fuel coverage selected: `Electric(Bov)` and `Pure Ev`, normalized to `ELECTRIC`
- Hybrid fuel labels: excluded from the EV run

## 5. Record counts and results

- Raw record count: 418,372 all-fuel rows
- Filtered EV source rows: 56,767
- Processed record count: 56,767
- Rejected record count: 0
- Total EV registrations represented: 17,572,522
- Validation status: WARNING only; no validation errors
- Warning: 56,760 rows share aggregation keys because the source is split by date/state/office/fuel dimensions; those rows are retained and summed by the analytics layer

## 6. Resume-claim assessment

- 10+ years supported: **NO**. The acquired file contains 6 years, 2019-2024.
- 20+ states supported: **YES**. The acquired file contains 34 states/UTs with accepted EV rows.
- Adoption supported: **NO**. The file contains EV registrations but no appropriate total-vehicle denominator.
- Supported wording: analyzed 2019-2024 state-level EV registration data across 34 states/UTs to calculate registration totals, growth, state contribution, and regional summaries.
- Unsupported wording: 10+ years and adoption rate. Manufacturer-level and vehicle-category claims are also unsupported by this selected resource.

## 7. Generated outputs

The pipeline generated outputs under `outputs/market/`:

- `yearly_market_growth.csv`
- `state_analysis.csv`
- `state_year_growth.csv`
- `manufacturer_analysis.csv` (empty because maker is not in this source)
- `category_analysis.csv` (empty because vehicle class is not in this source)
- `category_year_growth.csv`
- `regional_analysis.csv`
- `market_kpis.csv`
- `market_analysis_summary.md`

The cleaned accepted data and validation artifacts are under `data/processed/ev_market/`.
