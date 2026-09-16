# EV Market Data Methodology

## Scope

This methodology applies only to the historical EV market pipeline under `src/data/ev_market_pipeline.py`. It is separate from the existing verified product-catalog pipeline.

## Source and acquisition

The preferred source is a public Ministry of Road Transport & Highways / Parivahan / Vahan export. The source file must be downloaded through the publisher's normal public workflow and retained unchanged in `data/raw/ev_market/`. CAPTCHA, authentication, rate limits, and access restrictions must not be bypassed. Source metadata is recorded in `data/raw/ev_market/DATA_MANIFEST.md`.

No source export was present when this pipeline was implemented. Therefore this repository currently contains no new historical market result and makes no 10-year or 20-state claim from this pipeline.

## Accepted input

CSV, XLSX, and XLS files are supported. The source must provide `state`, `registrations`, and either `year` or a parseable `date`/`month`. Vehicle category, fuel type, and manufacturer are accepted when available and produce more granular outputs.

Column names are normalized to lowercase snake case using an explicit alias map. Common state aliases, category labels, fuel labels, and a small documented set of manufacturer aliases are normalized. Unknown values remain visible and produce validation warnings or errors; they are not silently discarded.

## Validation and cleaning

The pipeline:

- converts years and dates to numeric/datetime values
- rejects missing or out-of-range years
- rejects missing or unknown states
- converts registration counts with `pandas.to_numeric`; non-numeric and negative values are errors
- reports missing optional dimensions as warnings
- reports unexpected category and fuel values as warnings
- detects exact duplicate rows as errors
- reports duplicate aggregation keys as warnings because source exports may split a valid total across maker/fuel rows
- writes every rejected row to `data/processed/ev_market/rejected_records.csv`
- stops before analysis outputs when any error is present

No missing historical value is imputed. No suspicious row is silently removed.

## Aggregation and formulas

The pipeline produces yearly, state, manufacturer, category, and regional tables. Registrations are summed over the rows supplied by the source.

Year-over-year growth:

`(current year registrations - previous year registrations) / previous year registrations * 100`

CAGR over the observed first and last years:

`(ending registrations / starting registrations) ^ (1 / number of elapsed years) - 1`

Manufacturer market share is manufacturer registrations divided by total registrations for the analyzed dataset, multiplied by 100. State contribution uses the same denominator.

## Geographic mapping

The fixed mapping used by the code is:

- North: Chandigarh, Delhi, Haryana, Himachal Pradesh, Jammu and Kashmir, Ladakh, Punjab, Rajasthan, Uttar Pradesh, Uttarakhand
- South: Andaman and Nicobar Islands, Andhra Pradesh, Karnataka, Kerala, Lakshadweep, Puducherry, Tamil Nadu, Telangana
- East: Bihar, Jharkhand, Odisha, West Bengal
- West: Dadra and Nagar Haveli and Daman and Diu, Goa, Gujarat, Maharashtra
- Central: Chhattisgarh, Madhya Pradesh
- North-East: Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, Tripura

This is an analytical grouping, not a source-provided classification.

## Adoption terminology

Registration counts alone are not an EV adoption rate. The pipeline reports EV registrations, registration growth, registration contribution, and manufacturer/category shares. An adoption rate requires a denominator such as total vehicle registrations for the same geography and period:

`EV adoption rate = EV registrations / total vehicle registrations * 100`

The current pipeline does not calculate that rate unless a verified denominator is added and explicitly implemented. It does not infer adoption from EV registrations alone.

## Reproducibility

From the repository root:

```text
python src/data/ev_market_pipeline.py
```

Or select one input file:

```text
python src/data/ev_market_pipeline.py --input data/raw/ev_market/source_export.xlsx
```

Outputs are written to `data/processed/ev_market/` and `outputs/market/`. The command fails closed when no source export exists or when validation errors make the analysis unreliable.

## Coverage and limitations

The pipeline reports actual year and state coverage from the accepted source. It explicitly reports whether the data reaches 10+ years and 20+ states. It does not claim those thresholds when the supplied export does not contain them. Manufacturer and category outputs are unavailable or partial when those source columns are absent.
