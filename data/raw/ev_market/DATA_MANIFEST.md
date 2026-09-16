# EV Market Data Manifest

Complete this record for every source export placed in this directory. Do not mark a source official without verifying its publisher and source page.

| Field | Value |
|---|---|
| Dataset filename | `tdc_vahan_vehicle_registrations_by_fuel_type.csv` |
| Dataset name | Vahan Vehicle Registrations - India, by fuel type |
| Publisher/distributor | Transport Data Commons CKAN portal |
| Original publisher | Ministry of Road Transport & Highways / Parivahan Vahan |
| Original source | https://vahan.parivahan.gov.in/vahan4dashboard/ |
| Download URL | https://ckan.tdc.prod.datopian.com/dataset/111bf9f0-7268-4c27-ab58-29701b18a33a/resource/9597f1c6-0500-4558-bc90-105a95a3619a/download/vahan-vehicle-registrations-by-fuel-type-nmiqeb.csv |
| Download date (UTC) | 2026-09-16 |
| Original format | CSV |
| License or usage terms | No explicit license exposed in downloaded resource metadata; verify current terms before redistribution |
| Official or derived | DERIVED FROM OFFICIAL DATA; not a direct official Vahan export |
| Coverage start | 2019 |
| Coverage end | 2024 |
| Geographic coverage | 34 states/UTs with accepted EV rows |
| Vehicle/fuel filters | `Electric(Bov)` and `Pure Ev` normalized to `ELECTRIC`; hybrid labels excluded |
| Raw records | 418,372 all-fuel records |
| Filtered EV records | 56,767 |
| EV registrations represented | 17,572,522 |
| SHA-256 | `E502F671B5CD076F3A90EE15CA20113313758194C6FC9965EABF53144ECEC8A9` |
| Notes | Resource has date, state, fuel type, and registrations. It does not provide manufacturer or vehicle-class detail; source `category=Fuel` is not treated as a vehicle category. |

## Validation record

The pipeline writes the machine-generated validation report to:

`data/processed/ev_market/validation_report.json`

It also writes rejected source rows to:

`data/processed/ev_market/rejected_records.csv`

Generated validation record: WARNING only; 0 error checks, 1 duplicate-aggregation warning, 418,372 rows read, 56,767 EV rows after filter, 56,767 accepted, 0 rejected, 6 years (2019-2024), and 34 states. A source with validation errors must not be described as an analysis-ready dataset.
