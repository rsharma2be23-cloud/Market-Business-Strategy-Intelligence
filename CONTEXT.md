# Market-Business-Strategy-Intelligence

## 1. Project Overview

### 1.1 Project name
Market-Business-Strategy-Intelligence

### 1.2 One-paragraph description
This repository is an analytical and strategy intelligence project for the Indian electric two-wheeler market. It combines a verified product catalog, Python analytics, DuckDB SQL processing, Excel workbook outputs, and a Power BI project to analyze product pricing, manufacturer positioning, product-market fit, competitive intensity, and strategic opportunity. The project is explicitly designed to separate verified product data from pending registration-based market metrics and to avoid presenting unverified proxy data as factual market share or volume information.

### 1.3 Main business problem being solved
The repository addresses how to evaluate the Indian electric two-wheeler market from a commercial strategy perspective without relying on unsupported or fabricated market registration data. It gathers and standardizes verified manufacturer and model product intelligence, benchmarks price and range across the catalog, and supports strategy-oriented analysis while keeping market-share and growth metrics fail-closed until authoritative Vahan registration data is available.

### 1.4 Main objective
The main objective is to create an auditable commercial intelligence workflow for the Indian e2W market focused on verified product catalog analysis, price/value benchmarking, product positioning, competitive comparison, and strategic planning support.

### 1.5 Intended users / stakeholders
The project documentation indicates intended users include:
- business analysts
- strategy analysts
- analytics consultants
- product analysts
- management consultants
- executive decision-makers evaluating market entry or expansion

### 1.6 Domain / use case
Domain: Indian electric two-wheeler market, especially high-speed e-scooters and commercial model benchmarking.
Use case: business strategy, pricing analysis, competitive intelligence, product positioning, and scenario-based market-entry planning for the Indian e2W market.

### 1.7 Key outcomes the project is designed to provide
The project is designed to provide:
- verified manufacturer and product catalog benchmarking
- price, battery, and range comparison across models
- product positioning and whitespace analysis
- competitive intensity and portfolio concentration metrics
- KPI registry for verified outputs
- Excel workbook outputs for strategic review
- Power BI dashboard for interactive analysis
- fail-closed templates for future Vahan-based registration metrics

---

## 2. Project Architecture

### 2.1 Major components
The actual repository contains these major components:
- Python analytics under src/
- SQL analytics under sql/
- processed and raw data under data/
- Power BI project under powerbi/
- documentation under docs/
- generated outputs under outputs/
- verification artifacts at the root, including pytest_out.txt and quick_verify.py

### 2.2 Data flow from input to final output
Raw and processed data are organized in a clear flow:

Input catalog and source files
   ↓
Python validation and normalization
   ↓
DuckDB SQL schema and analytical marts
   ↓
CSV output marts and KPI tables
   ↓
Excel workbook generation
   ↓
Power BI semantic model and DAX measures
   ↓
Dashboard/report outputs and business insight artifacts

Text-based architecture diagram:

Verified OEM product data
   ↓
Python data validation and transformation
   ↓
DuckDB staging + fact/dimension schemas
   ↓
SQL marts: competitive, pricing, positioning, KPI status
   ↓
Processed CSV outputs
   ↓
Excel workbook and Power BI dashboard
   ↓
Strategic business analysis and reporting

### 2.3 Python components
Python code exists in src/ and under src/analytics/.

Main Python modules and their roles:
- src/data_processing.py: validates and standardizes raw datasets, creates processed files, computes template outputs, and writes validation_results.json.
- src/run_sql_pipeline.py: runs the SQL pipeline, loads the DuckDB database, validates quality checks, and exports CSV outputs.
- src/generate_excel_workbook.py: builds the Excel workbook from SQL marts and companion tables.
- src/market_data_ingestion.py: present in the repo but not fully documented as a standalone runtime script beyond the repository structure.
- src/populate_raw_datasets.py: present in the repo but not fully documented as a standalone runtime script beyond the repository structure.

Analytics modules under src/analytics/:
- competitive_analysis.py
- geographic_analysis.py
- kpi_engine.py
- market_analysis.py
- positioning_analysis.py
- pricing_analysis.py
- scenario_analysis.py
- strategic_analysis.py
- unit_economics.py

These modules implement the product analytics, KPI registry, pricing analysis, segmentation, geographic scoring framework, and strategic ideas. Several functions explicitly guard against unsupported inputs by returning pending templates instead of fabricated metrics.

### 2.4 SQL components
The sql/ directory contains the analytical warehouse scripts:
- 01_schema.sql: schema creation, table/view drops, and initial warehouse model
- 02_load_verified_data.sql: loads verified product data into staging tables and fact/dimension tables
- 03_data_quality.sql: enforces quality checks and writes sql_data_quality_results
- 04_competitive_analysis.sql: computes competitive analysis view
- 05_pricing_analysis.sql: computes pricing mart and relative pricing metrics
- 06_product_positioning.sql: computes product position and segmentation view
- 07_kpi_queries.sql: computes verified KPI outputs and HHI status
- 08_pending_market_queries.sql: creates a fail-closed pending schema and SQL templates for future Vahan registration analysis

### 2.5 Data processing / analytics components
The project includes both Python and SQL processing components. The repository’s pattern is:
- raw source files stored in data/raw/
- Python preprocessing in src/data_processing.py
- DuckDB warehouse execution in src/run_sql_pipeline.py
- CSV marts under data/processed/sql/
- Excel workbook generated from those marts
- dashboard and semantic model fed by those outputs

### 2.6 Power BI components
Power BI artifacts are located in powerbi/:
- Market-Business-Strategy-Intelligence.pbip
- Market-Business-Strategy-Intelligence.Report/
- Market-Business-Strategy-Intelligence.SemanticModel/
- dax_measures.dax
- power_query_m_scripts.m
- validate_pbip.py
- generate_model_bim.py
- patch_pbip_paths.py

The repository includes report definitions and a semantic model definition, plus validation scripts. It does not include a compiled .pbix binary in the repository tree.

### 2.7 Notebooks
The repository includes one notebook:
- prompt_3a_verification.ipynb

From the notebook summary, none of the cells were executed in the current editor state. It appears to be a verification or analysis notebook, but the repository does not provide execution output or final conclusions embedded in the notebook itself.

### 2.8 Scripts
Important project scripts:
- quick_verify.py: runs pytest on the project and exits with the pytest code
- src/data_processing.py: end-to-end processing script
- src/run_sql_pipeline.py: runs all SQL scripts
- src/generate_excel_workbook.py: generates outputs/Market_Business_Strategy_Intelligence.xlsx
- powerbi/validate_pbip.py: validates the PBIP report structure and model metadata
- powerbi/generate_model_bim.py: likely generates or patches model definitions, but the exact runtime workflow is not fully described in the repo
- powerbi/patch_pbip_paths.py: patching script for local Power BI paths

### 2.9 External tools / services
Explicitly referenced in the repository:
- DuckDB (embedded analytical database)
- Python + pandas + numpy + xlsxwriter + pytest
- Power BI Desktop / PBIP project files
- Vahan public dashboard URL in documentation as an external source to be manually retrieved if available
- MoRTH/Vahan, Ministry of Heavy Industries, and other public government and OEM sources referenced in docs
- Internet data sources for OEM pages and policy notices

### 2.10 Relationships and dependencies between components
The actual dependency structure is:
- Raw source files feed into Python validation scripts.
- Python scripts generate processed CSVs and templates.
- SQL scripts read those CSVs and create data warehouse tables and marts.
- CSV marts are exported to data/processed/sql/.
- The Excel workbook reads those marts and creates a workbook artifact.
- Power BI consumes the mart outputs and the semantic model definitions.
- Documentation explains the business logic, provenance policy, and governance constraints.
- Validation scripts confirm structural correctness and fail-closed behavior.

---

## 3. Repository Structure

Important repository directories and files:

```text
Market-Business-Strategy-Intelligence/
├── README.md
├── CONTEXT.md
├── implementation_plan.md
├── requirements.txt
├── quick_verify.py
├── pytest_out.txt
├── prompt_3a_verification.ipynb
├── data/
│   ├── processed/
│   │   ├── competitive_intensity.csv
│   │   ├── competitive_kpis.csv
│   │   ├── geographic_scoring_template.csv
│   │   ├── kpi_registry.csv
│   │   ├── kpi_status.csv
│   │   ├── manufacturer_kpis.csv
│   │   ├── pricing_kpis.csv
│   │   ├── processed_competitor_specs.csv
│   │   ├── processed_market_hhi.csv
│   │   ├── processed_oem_market_shares.csv
│   │   ├── processed_policy_timeline.csv
│   │   ├── processed_state_indicators.csv
│   │   ├── processed_vahan_monthly.csv
│   │   ├── processed_verified_product_catalog.csv
│   │   ├── product_positioning.csv
│   │   ├── product_value_scores.csv
│   │   ├── scenario_analysis_template.csv
│   │   ├── strategic_priority_template.csv
│   │   ├── unit_economics_input_template.csv
│   │   ├── unit_economics_results.csv
│   │   ├── unit_economics_template.csv
│   │   ├── validation_results.json
│   │   ├── verified_product_catalog_canonical.csv
│   │   └── sql/
│   │       ├── e2w_sql.duckdb
│   │       ├── sql_competitive_analysis.csv
│   │       ├── sql_data_quality_results.csv
│   │       ├── sql_kpi_results.csv
│   │       ├── sql_pipeline_summary.json
│   │       ├── sql_pricing_analysis.csv
│   │       └── sql_product_positioning.csv
│   └── raw/
│       ├── DATASET_MANIFEST.csv
│       ├── competitor_product_catalog.csv
│       ├── oem_e2w_registrations_annual.csv
│       ├── policy_incentive_timeline.csv
│       ├── state_socioeconomic_indicators.csv
│       ├── vahan_e2w_registrations_monthly.csv
│       ├── verified_product_catalog_2025_2026.csv
│       └── market_registrations/
│           └── (directory present; exact contents not enumerated in this repo snapshot)
├── docs/
│   ├── ANALYTICAL_ENGINE.md
│   ├── DATA_ACQUISITION_GUIDE.md
│   ├── DATA_DICTIONARY.md
│   ├── DATA_SOURCE_REGISTER.md
│   ├── EXCEL_ANALYSIS.md
│   ├── FINAL_DATA_ACQUISITION_REPORT.md
│   ├── FINAL_KPI_REGISTRY.md
│   ├── GEOGRAPHIC_ANALYSIS.md
│   ├── KPI_FRAMEWORK.md
│   ├── POWER_BI_DASHBOARD_SPEC.md
│   ├── POWER_BI_DAX.md
│   ├── POWER_BI_KPI_MAPPING.md
│   ├── POWER_BI_MODEL.md
│   ├── POWER_BI_POWER_QUERY.md
│   ├── PRODUCT_POSITIONING.md
│   ├── RESUME_CLAIM_AUDIT.md
│   ├── RESUME_CLAIM_VALIDATION.md
│   ├── SOURCE_INVESTIGATION_REPORT.md
│   ├── SQL_ANALYTICS.md
│   ├── STRATEGIC_ANALYSIS.md
│   └── UNIT_ECONOMICS.md
├── outputs/
│   └── Market_Business_Strategy_Intelligence.xlsx
├── powerbi/
│   ├── dax_measures.dax
│   ├── generate_model_bim.py
│   ├── patch_pbip_paths.py
│   ├── power_query_m_scripts.m
│   ├── validate_pbip.py
│   ├── Market-Business-Strategy-Intelligence.pbip
│   ├── Market-Business-Strategy-Intelligence.Report/
│   │   ├── definition.pbir
│   │   └── definition/
│   │       └── report.json
│   └── Market-Business-Strategy-Intelligence.SemanticModel/
│       └── definition/
│           └── model.bim
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load_verified_data.sql
│   ├── 03_data_quality.sql
│   ├── 04_competitive_analysis.sql
│   ├── 05_pricing_analysis.sql
│   ├── 06_product_positioning.sql
│   ├── 07_kpi_queries.sql
│   └── 08_pending_market_queries.sql
├── src/
│   ├── data_processing.py
│   ├── generate_excel_workbook.py
│   ├── market_data_ingestion.py
│   ├── populate_raw_datasets.py
│   ├── run_sql_pipeline.py
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── competitive_analysis.py
│   │   ├── geographic_analysis.py
│   │   ├── kpi_engine.py
│   │   ├── market_analysis.py
│   │   ├── positioning_analysis.py
│   │   ├── pricing_analysis.py
│   │   ├── scenario_analysis.py
│   │   ├── strategic_analysis.py
│   │   └── unit_economics.py
│   └── tests/
│       └── test_data_processing.py
└── .gitignore
```

### 3.1 What each directory/file contains and why it matters
- README.md: high-level explanation of the repository and project narrative.
- implementation_plan.md: blueprint and strategic plan for the project.
- requirements.txt: Python dependencies for the project.
- data/raw/: original source files and legacy/proxy datasets retained for provenance review.
- data/processed/: cleaned, standardized, and generated analytical datasets.
- docs/: the project’s analytical, data-source, KPI, and dashboard documentation.
- outputs/: generated business outputs, including the final Excel workbook.
- powerbi/: the PBIP project, semantic model, DAX measures, report definitions, and validation scripts.
- sql/: the DuckDB schema and data transformation pipeline.
- src/: Python implementation, validation, workbook generation, and analytics logic.
- pytest_out.txt: raw pytest output artifact.
- prompt_3a_verification.ipynb: notebook used for verification steps, currently not executed in the editor state.

---

## 4. Technologies and Tools

### 4.1 Programming languages
- Python: primary language for ETL, validation, KPI generation, and workbook generation.
- SQL: DuckDB SQL scripts for transformations, marts, and fail-closed market query templates.
- DAX: Power BI measure definitions and model logic.
- M language: Power Query scripts are present in powerbi/power_query_m_scripts.m.
- JSON: model/report definitions and validation outputs are stored as JSON.

### 4.2 Python libraries
From requirements.txt:
- duckdb>=1.0.0
- pandas>=2.0.0
- xlsxwriter>=3.1.0
- pytest>=8.0.0
- numpy>=1.24.0

These are used for:
- database operations and CSV ingestion
- tabular transformation and validation
- Excel workbook generation
- automated testing
- numeric computations for KPI and metric generation

### 4.3 Data and analytics tools
- DuckDB: used as the in-process analytical warehouse.
- Pandas: used for reading and shaping CSVs and producing processed outputs.
- NumPy: used for numeric operations and safe numeric conversions.
- Power BI: used for semantic model, DAX measures, and dashboard/report implementation.

### 4.4 SQL / database technologies
- DuckDB SQL scripts in sql/
- schema names: raw, stg, mart, kpi, pending
- fail-closed future market registration table: pending.fact_ev_registrations

### 4.5 Visualization / BI
- Power BI PBIP + report definition + SemanticModel definition
- DAX measures stored in powerbi/dax_measures.dax
- Power Query scripts in powerbi/power_query_m_scripts.m

### 4.6 Notebooks
- Jupyter / IPython notebook: prompt_3a_verification.ipynb

### 4.7 Development tools
- Git repository metadata (not described in detail because the instructions exclude Git internals from the repository context document)
- pytest for verification and regression-style checks
- quick_verify.py for running the test suite

### 4.8 Testing / verification
- pytest (configured through quick_verify.py)
- data validation JSON output at data/processed/validation_results.json
- PBIP validation script at powerbi/validate_pbip.py
- SQL data-quality checks in sql/03_data_quality.sql

### 4.9 External services / APIs
The repository documentation references several external services but does not contain actual API keys or secrets:
- Vahan public dashboard (MoRTH)
- data.gov.in API endpoints (mentioned as an external option in source investigation materials)
- Ministry of Heavy Industries notices and documents
- OEM public product pages, brochures, and investor disclosures
- RBI / MoSPI / NITI Aayog references in policy and geographic analysis docs

---

## 5. Data

### 5.1 Data sources actually present or referenced
The repository contains both verified and quarantined datasets. The actual documented source hierarchy is:

1. Verified product catalog (primary source data used in the final analytics)
2. Legacy unverified / proxy datasets intentionally quarantined
3. Pending market registration datasets intentionally not loaded as factual data

### 5.2 Verified product catalog
- Name: verified_product_catalog_2025_2026.csv
- Location: data/raw/verified_product_catalog_2025_2026.csv
- Format: CSV
- Purpose: verified catalog of electric two-wheeler products used as the factual source for product benchmarking
- Important fields: manufacturer, model_name, vehicle_category, ex_showroom_price_inr, price_basis, battery_capacity_kwh, range_km, range_standard, top_speed_kmh, motor_peak_power_kw, launch_status, source_url, source_type, accessed_date, verification_status, verification_notes
- Approximate size: 42 rows in data/processed/validation_results.json; this is the processed verified catalog dataset
- Relationships: forms the basis for stg_verified_products in SQL and all downstream pricing, positioning, and KPI tables
- Preprocessing: validated and standardized in src/data_processing.py; verification_status enforced to verified
- Missing values: explicitly recorded as present in validation_results.json; for example ex_showroom_price_inr has 8 missing values
- Transformations: types cast, field normalization, provenance metadata retained
- Assumptions: only verified catalog rows are used for factual analytics; blank values mean the source did not support the field

### 5.3 Processed verified product catalog
- Name: processed_verified_product_catalog.csv
- Location: data/processed/processed_verified_product_catalog.csv
- Format: CSV
- Purpose: processed version of the verified product catalog for downstream SQL and analytics
- Important fields: same schema as the raw verified catalog, with provenance and dataset metadata added in processing

### 5.4 Legacy / proxy datasets retained for governance purposes
These datasets are present in data/raw and data/processed but are explicitly marked as not eligible as observed analytics:

#### vahan_e2w_registrations_monthly.csv
- Location: data/raw/vahan_e2w_registrations_monthly.csv
- Format: CSV
- Purpose: legacy generated proxy dataset, not accepted as factual market data
- Status: provenance_class = generated_proxy; eligible_as_observed_analytics = No
- Approximate size: 1368 rows in validation_results.json
- Important fields: year, month, year_month, state, state_code, e2w_registrations, total_2w_registrations, data_source

#### oem_e2w_registrations_annual.csv
- Location: data/raw/oem_e2w_registrations_annual.csv
- Format: CSV
- Purpose: legacy generated OEM registration proxy
- Status: generated_proxy; ineligible as observed analytics
- Approximate size: 59 rows
- Important fields: year, oem_name, oem_category, e2w_registrations, data_source

#### competitor_product_catalog.csv
- Location: data/raw/competitor_product_catalog.csv
- Format: CSV
- Purpose: legacy manual compilation, superseded by verified catalog
- Status: manual_compilation_unverified; ineligible as observed analytics
- Approximate size: 31 rows

#### state_socioeconomic_indicators.csv
- Location: data/raw/state_socioeconomic_indicators.csv
- Format: CSV
- Purpose: state-level indicators for analytical templates and scenario design
- Status: generated_proxy; ineligible as observed analytics
- Important fields: state, state_code, population_2024_est_millions, data_source

#### policy_incentive_timeline.csv
- Location: data/raw/policy_incentive_timeline.csv
- Format: CSV
- Purpose: policy timeline references for PM E-DRIVE/FAME-related reasoning
- Status: source_transcription_pending_document; not eligible as observed analytics
- Important fields: policy_scheme, start_date, end_date, data_source

### 5.5 Data processed outputs in data/processed/
These datasets are used for business analysis and include:
- processed_market_hhi.csv
- processed_oem_market_shares.csv
- processed_policy_timeline.csv
- processed_state_indicators.csv
- processed_vahan_monthly.csv
- processed_verified_product_catalog.csv
- product_positioning.csv
- product_value_scores.csv
- unit_economics_input_template.csv
- unit_economics_results.csv
- scenario_analysis_template.csv
- strategic_priority_template.csv
- validation_results.json
- competitive_intensity.csv
- kpi_status.csv

### 5.6 Data quality and provenance notes
The project has strict provenance logic. According to DATASET_MANIFEST.csv:
- verified_primary_source data is marked as eligible_as_observed_analytics = Yes
- generated_proxy and manual_compilation_unverified rows are marked as No
- pending policy documents are marked as source_transcription_pending_document

The validation output confirms the verified dataset has zero errors and 42 rows, while the unverified datasets are retained only as legacy references.

---

## 6. Data Pipeline

The repository’s actual data pipeline steps are:

1. Data acquisition
   - Source files are stored under data/raw/
   - OEM product pages and public product disclosures form the verified primary source set
   - Legacy proxy datasets remain in raw but are not treated as factual analytics

2. Data validation
   - src/data_processing.py audits required columns, missing values, duplicate rows, and invalid numeric rows
   - data/raw/DATASET_MANIFEST.csv classification is used to assign provenance flags
   - validation_results.json records dataset-level validation results

3. Data cleaning and standardization
   - state names are normalized using a mapping in src/data_processing.py
   - numeric conversions are applied to price, battery, range, and power columns
   - provenance metadata is attached to processed tables

4. Transformation and feature creation
   - SQL loads verified catalog into stg_verified_products, dim_product, dim_manufacturer, and fact_product_metrics
   - price_per_km, price_per_kwh, and wh_per_km are created in SQL
   - product positioning bucket logic is calculated in 06_product_positioning.sql

5. KPI and metric creation
   - 07_kpi_queries.sql computes verified KPIs such as manufacturer count, product count, average price, average battery, average range, and product portfolio HHI
   - kpi_status is written as a KPI register

6. SQL analysis
   - competitive, pricing, and positioning views are produced
   - additional pending market templates are created in 08_pending_market_queries.sql

7. Business analysis
   - docs/FINAL_KPI_REGISTRY.md, docs/KPI_FRAMEWORK.md, and docs/STRATEGIC_ANALYSIS.md document the intended strategic analysis
   - business recommendations are assembled in src/generate_excel_workbook.py

8. Dashboard generation
   - processed CSV outputs feed into Power BI semantic model and DAX measures
   - report.json defines the five report pages
   - outputs/Market_Business_Strategy_Intelligence.xlsx is generated from the SQL marts

9. Final outputs
   - workbook artifact in outputs/
   - SQL outputs in data/processed/sql/
   - dashboard project files under powerbi/
   - documentation under docs/

---

## 7. SQL Analysis

### 7.1 Tables and schema
The SQL warehouse uses the following schema structure:
- raw: reserved for raw data context
- stg: stg_verified_products staging table
- mart: mart_competitive_analysis, mart_pricing_analysis, mart_product_positioning
- kpi: kpi_status view/table
- pending: pending.fact_ev_registrations and pending.market_queries_template

Important table definitions from 01_schema.sql:
- stg_verified_products
- dim_manufacturer
- dim_product
- fact_product_metrics
- sql_data_quality_results

Important fields in stg_verified_products:
- manufacturer
- model_name
- vehicle_category
- ex_showroom_price_inr
- price_basis
- battery_capacity_kwh
- range_km
- range_standard
- top_speed_kmh
- motor_peak_power_kw
- launch_status
- source_url
- source_type
- accessed_date
- verification_status
- verification_notes
- source_dataset
- provenance_class
- eligible_as_observed_analytics
- source

### 7.2 Important queries and business logic
#### 04_competitive_analysis.sql
This view compares manufacturers and products using window functions:
- ROW_NUMBER() over manufacturer by price
- DENSE_RANK() over overall price
- RANK() over price_per_km
- RANK() over certified_range_km
- RANK() over top_speed_kmh
- COUNT(*) over manufacturer and portfolio share

It answers questions like:
- which products are cheapest within a manufacturer?
- which models are most efficient by price-per-km?
- which vehicles occupy the highest range or speed positions?

#### 05_pricing_analysis.sql
This view calculates price distribution and pricing buckets:
- PERCENT_RANK() over price
- NTILE(4) over price
- AVG(ex_showroom_price_inr) over all products
- AVG(ex_showroom_price_inr) over manufacturer
- price_bucket classification (budget, mid-market, premium)
- relative_price_position and price_premium_vs_market_pct

This is the core benchmark layer for pricing analysis.

#### 06_product_positioning.sql
Creates product position buckets by price, range, battery, and performance. It uses:
- price_bucket
- range_bucket
- battery_bucket
- performance_bucket
- positioning_summary
- manufacturer_product_rank and portfolio share metrics

This supports segmentation and whitespace analysis.

#### 07_kpi_queries.sql
Produces kpi_status with verified indicators:
- manufacturer_count
- product_count
- priced_product_count
- average_price_inr
- median_price_inr
- min_price_inr
- max_price_inr
- average_battery_kwh
- average_range_km
- average_top_speed_kmh
- average_motor_power_kw
- average_price_per_km
- average_price_per_kwh
- product_portfolio_hhi

These values match the current repo outputs in data/processed/sql/sql_kpi_results.csv.

#### 08_pending_market_queries.sql
This is the fail-closed market layer. It creates a pending schema with:
- pending.fact_ev_registrations table with 0 rows by design
- pending.market_queries_template with SQL templates for market volume, growth, CAGR, EV penetration, OEM market share, HHI, and state ranking

The actual database enforces a no-proxy policy: the table is empty and the repository states this is intentional.

### 7.3 Joins, aggregations, CTEs, and window functions
The SQL scripts use common pattern elements:
- CTEs for segmentation and ranking logic
- aggregation via GROUP BY and COUNT, AVG, MIN, MAX, MEDIAN
- window functions: ROW_NUMBER, DENSE_RANK, RANK, PERCENT_RANK, NTILE, AVG OVER, COUNT OVER, SUM OVER
- no materialized views other than explicit CREATE OR REPLACE VIEW statements

### 7.4 Business questions answered by SQL
The repository’s SQL analysis explicitly supports questions such as:
- Which manufacturers have the broadest product portfolios?
- Which products are best positioned by price and range?
- Which product segments are under- or over-priced relative to the catalog average?
- What is the product portfolio concentration score (HHI)?
- What are the verified product KPI benchmarks?

The market-registration questions are all intentionally left as template queries because the required data is not present in the repository.

---

## 8. Business Analysis

### 8.1 Market analysis
The repository includes strategic documentation about the Indian electric two-wheeler market, including policy shifts, growth drivers, and vehicle market structure. The actual project documentation references:
- FAME-II transition and PM E-DRIVE context
- commercialization and pricing expectations
- geographic attractiveness frameworks
- scenario analysis for policy, battery cost, and petrol price effects

However, the actual repository does not contain a verified, full market registration series for e2W market size or OEM market share. The market volume and state growth layers remain pending.

### 8.2 Competitive analysis
This project does compare verified product offerings across manufacturers and models using the product catalog. It calculates:
- manufacturer portfolio counts
- price rank by manufacturer
- range ranks
- speed ranks
- product portfolio HHI
- relative price position

### 8.3 Pricing analysis
The pricing analysis is a central project pillar. It uses ex_showroom_price_inr, battery_capacity_kwh, and range_km to calculate:
- price_per_km
- price_per_kwh
- price_bucket
- price_percentile
- price_quartile
- relative price position
- price_premium_vs_market_pct

Key price buckets are defined in SQL as:
- budget: price < 100000
- mid-market: 100000 <= price <= 180000
- premium: price > 180000

### 8.4 Growth analysis
The documentation and SQL templates describe growth analysis using Vahan registration data, but no verified Vahan registration dataset is present in the repository. Therefore, actual growth metrics are not calculated from official market data here; the growth functions remain templates and fail-closed.

### 8.5 Customer analysis
The project documentation positions the analysis around commuter demand, B2B fleet needs, pricing sensitivity, and deployment strategy, but no customer-level dataset is present in the repo. This part is conceptual and framed as strategic analysis rather than actual observed customer data analysis.

### 8.6 Revenue analysis
The repository includes indicative pricing and cost frameworks, but actual revenue or margin results dependent on proprietary or external input data are not present as complete, verified datasets. Scenario and unit economics templates are included, but they remain model-based frameworks rather than actual observed revenue metrics.

### 8.7 Market segmentation
Actual segmentation implemented in the repo:
- price_bucket
- range_bucket
- battery_bucket
- performance_bucket

These maps are used in product_positioning.csv and SQL mart_product_positioning.

### 8.8 KPIs
Verified KPIs are in data/processed/sql/sql_kpi_results.csv and include:
- manufacturer_count = 11
- product_count = 42
- priced_product_count = 34
- average_price_inr = 136349.21
- median_price_inr = 126170.5
- min_price_inr = 74990.0
- max_price_inr = 399000.0
- average_battery_kwh = 3.73
- average_range_km = 159.39
- average_top_speed_kmh = 89.17
- average_motor_power_kw = 8.02
- average_price_per_km = 867.71
- average_price_per_kwh = 36418.79
- product_portfolio_hhi = 1326.53

### 8.9 Strategic recommendations
The repo includes strategy-oriented recommendation logic in src/generate_excel_workbook.py. These recommendations are explicit and tied to verified product catalog and pricing evidence. They do not claim that market-share or Vahan-based outcomes have been verified.

### 8.10 Business interpretation supported by the repository
Supported by actual datasets and code:
- the catalog is dominated by mid-market pricing tiers
- price-per-km and battery/range comparisons vary widely across models
- the verified catalog includes budget, mid-market, and premium segments
- product portfolio concentration is measured by HHI using product counts rather than official market registration data

Not supported by the repo as factual outputs:
- market-share by OEM from Vahan
- year-over-year registration growth
- national/state e2W market size and penetration

---

## 9. Power BI / Dashboard

### 9.1 Dashboard purpose
The Power BI project is intended to present the verified product-catalog market intelligence, competitive benchmarking, pricing/value analysis, positioning, and strategic opportunity framework.

### 9.2 Pages
The repository documentation and report.json indicate five report pages:
1. Executive Market & Business Overview
2. Product & Competitive Intelligence
3. Pricing & Value Analysis
4. Product Positioning & Whitespace Analysis
5. Strategy & Opportunity Framework

### 9.3 Visuals and KPIs
Power BI validation script checks for 5 pages and at least 30 visual containers. The repository states:
- 39 visual containers
- 35 DAX measures
- 5 pages

The project documentation names multiple KPI cards and visuals associated with price, range, value, and competitive benchmarking.

### 9.4 Filters / slicers
The project documentation indicates use of slicers and filter context for manufacturer, segment, price bucket, and performance factors; the exact slicer list is not enumerated in the repo text. Not enough detail is available to reconstruct the full visual slicer model with certainty.

### 9.5 Measures and DAX
The repository contains:
- powerbi/dax_measures.dax
- docs/POWER_BI_DAX.md

The docs describe many DAX measures, including:
- Total Products
- Total Manufacturers
- Priced Products Count
- Average Product Price
- Median Product Price
- Minimum Product Price
- Maximum Product Price
- Average Battery Capacity
- Average Certified Range
- Average Top Speed
- Average Motor Power
- Average Price per KM
- Average Price per KWh
- Product Portfolio HHI

The actual number of DAX measures in the model definitions is not fully enumerated in this repository without opening the generated model more deeply than the repo text provides, but the validation script and documentation describe a final total of 35 measures.

### 9.6 Calculated columns
Power BI docs indicate a star schema with dimensions and fact tables. The repository text describes use of calculated columns only sparingly, especially for audit and categorical slices. The exact list of model columns is not fully enumerated in the repo text beyond the documented tables.

### 9.7 Data model
The documentation describes a star schema with:
- DimManufacturer
- DimProduct
- FactProductMetrics
- CompetitiveAnalysis
- PricingAnalysis
- ProductPositioning
- KPIStatus
- PendingMarketRegistrations

The model is designed to keep pending registration data fail-closed and isolated.

### 9.8 Relationships
The repo documentation describes one-direction star schema relationships from dimension tables to fact tables and from fact tables to extension tables, with no bidirectional cross-filtering. This is documented in docs/POWER_BI_MODEL.md.

### 9.9 Data sources
The actual Power BI model is fed from local CSV marts under data/processed/sql and from the verified product catalog workflow. There is no evidence of external live Power BI data sources in the repository.

### 9.10 Important insights and limitations
The repo states that the dashboard was repaired and validated locally with five pages and KPI cards populated. It also explicitly says the market registration and growth measures remain pending because no verified Vahan market dataset was loaded into the repository.

Important limitation: the actual PBIP and semantic model can be inspected as source files, but the full rendered report itself cannot be directly opened in this environment; the repository documents the intended structure and validation states.

---

## 10. Python Code

### 10.1 Main scripts and their purpose
- src/data_processing.py: validates raw datasets and creates processed outputs; writes validation_results.json.
- src/run_sql_pipeline.py: executes the full SQL warehouse pipeline and exports results to data/processed/sql/.
- src/generate_excel_workbook.py: builds the final Excel workbook artifact.
- quick_verify.py: runs pytest across the project and returns the exit code.

### 10.2 Functions and analytical logic
The main Python modules in src/analytics implement specifics:
- pricing_analysis.py: functions for price percentiles, range percentiles, battery percentile, and value score computation
- positioning_analysis.py: price/range/performance/battery segmentation and whitespace analysis
- geographic_analysis.py: GAI template and weighting structure for state attractiveness scoring
- strategic_analysis.py: competitive intensity score and strategic priority template logic
- kpi_engine.py: KPI registry and KPI computations with pending status for non-verified metrics
- unit_economics.py: scenario-based cost and margin logic; uses assumptions and templates, not verified market data
- market_analysis.py: likely includes market calculations, but the repository text does not provide a complete runtime description for all custom functions

### 10.3 Inputs and outputs
Inputs:
- dataset files under data/raw/
- manifest at data/raw/DATASET_MANIFEST.csv
- sample values from verified catalog and legacy datasets

Outputs:
- processed CSV files in data/processed/
- SQL marts in data/processed/sql/
- validation_results.json
- Excel workbook in outputs/

### 10.4 Important algorithms
The actual algorithms in code include:
- provenance audit with column checks and duplicate row detection
- normalized state mapping for geographic fields
- price-per-range and price-per-battery calculations
- min-max normalization for scoring templates
- product segmentation and whitespace classification
- HHI calculation using shares squared
- fail-closed logic where missing verified market data results in pending-templates behavior rather than fabricated data

### 10.5 Error handling and configuration
The code explicitly models safeguards instead of silently inventing values:
- if required verified inputs are missing, functions return pending-data templates
- SQL pipeline aborts on data quality failures
- pending market registration tables are kept empty
- provenance classification is enforced instead of hiding legacy or proxy sources

### 10.6 Dependencies
The Python code depends on:
- pandas
- numpy
- duckdb
- xlsxwriter
- pytest

No hidden runtime dependencies or secrets were found in the repository.

---

## 11. Notebooks

### 11.1 prompt_3a_verification.ipynb
- Purpose: repository-level verification workflow and analysis notebook
- Inputs: data files and project analytics
- Processing steps: not executed in the current editor state, based on notebook summary
- Analysis performed: not available as executed output; notebook content was not executed in the repository context
- Important outputs: none are present in the notebook summary
- Libraries used: likely pandas, numpy, and other data-science libraries, but these are not explicitly documented in repo output
- Final conclusions/results: not available because no cells were executed in the current state

The notebook is present but does not demonstrate a completed end-to-end executed result in this workspace state.

---

## 12. Verification and Testing

### 12.1 Test files and scripts
- src/tests/test_data_processing.py: present in the repository tree, but the exact file path and direct read were not fully resolvable from the initial inspection because the repo snapshot included a tests directory but this file path was not available to read in the current environment. The repository structure confirms a test file is intended to exist.
- quick_verify.py: runs pytest on the project
- powerbi/validate_pbip.py: verifies PBIP model structure, page count, and measure presence
- sql/03_data_quality.sql: ensures data quality checks are enforced in SQL
- data/processed/validation_results.json: generated validation output
- pytest_out.txt: output log from pytest execution

### 12.2 Actual verification status from repository evidence
The repository contains the following explicit validation results:
- data/processed/validation_results.json shows six source datasets were validated; all had zero errors on the verified data path
- Power BI validation script checks exist and expect 5 pages, the executive page, competitive page, pricing page, positioning page, strategy page, and 30+ visual containers
- SQL pipeline is designed to halt if any required data quality checks fail
- README and docs mention 39 automated tests and 14/14 PBIP integrity checks, but the raw pytest log was not read cleanly enough to confirm the exact count in this environment; the repository text and outputs indicate this is the intended status

### 12.3 Data quality checks
The SQL data quality checks in 03_data_quality.sql include:
- duplicate_products
- duplicate_manufacturer_model
- null_required_fields
- negative_prices
- invalid_battery_capacities
- invalid_ranges
- invalid_speed_values
- invalid_motor_power
- unverified_records
- missing_provenance

These checks are enforced in the DuckDB pipeline and the script aborts if issue_count > 0.

### 12.4 Known limitations in verification
- The repo does not contain official Vahan registration data, so market-share and growth analyses remain intentionally unverified.
- The notebook is not executed in the current workspace state.
- The exact pass count from pytest_out.txt is not cleanly readable in the raw output; the docs provide the expected status but the raw file is not a reliable final confirmation source.

---

## 13. Outputs

### 13.1 outputs/Market_Business_Strategy_Intelligence.xlsx
- What it is: final Excel workbook used for analytical summary review
- How generated: created by src/generate_excel_workbook.py using SQL mart CSVs
- What it represents: strategic workbook with KPI summary, competitive benchmark, pricing analysis, product positioning, strategic recommendations, source register, and assumptions/provenance tables
- Interpretation: business-review artifact used alongside the Power BI dashboard and SQL marts
- Producer: Python workbook generation script and processed SQL data outputs

### 13.2 data/processed/sql/*.csv files
These act as the analytic marts used by Power BI and Excel:
- sql_competitive_analysis.csv
- sql_pricing_analysis.csv
- sql_product_positioning.csv
- sql_kpi_results.csv
- sql_data_quality_results.csv
- sql_pipeline_summary.json

These files capture the actual outputs of the SQL pipeline and are the primary intermediate artifacts between SQL and the final dashboard workbook.

### 13.3 data/processed/*.csv files
These are generated data products such as:
- processed_verified_product_catalog.csv
- processed_market_hhi.csv
- processed_oem_market_shares.csv
- product_positioning.csv
- product_value_scores.csv
- validation_results.json

These support analytics and are the basis for the project’s processed model.

### 13.4 Power BI outputs
The repository contains the source-controlled Power BI project files, but not a final compiled .pbix binary. The outputs are produced from the PBIP and report definition files plus the semantic model.

---

## 14. Configuration and Dependencies

### 14.1 requirements.txt
The actual dependency list is:
- duckdb>=1.0.0
- pandas>=2.0.0
- xlsxwriter>=3.1.0
- pytest>=8.0.0
- numpy>=1.24.0

### 14.2 Configuration files
The repository includes:
- .gitignore (present but not inspected in detail)
- requirements.txt
- project-specific CSV manifests and metadata files
- Power BI project metadata in the PBIP and model JSON files

### 14.3 Environment variables
No environment variable names are explicitly defined in the repository. There are no .env files or config files indicating runtime credentials or secrets.

### 14.4 External dependencies
- Power BI Desktop for opening the PBIP/report
- Python environment with the pinned libraries in requirements.txt
- Local file system access to data/raw and data/processed
- Optional access to external OEM and government websites for acquisition and source validation

### 14.5 Installation and runtime requirements
The repository expects a local Python environment and the packages listed in requirements.txt. It is not a cloud-hosted application and has no external deployment configuration in the repo.

---

## 15. How to Run the Project

### 15.1 Environment setup
From a clean environment:
1. Create a Python environment.
2. Install dependencies from requirements.txt.
3. Ensure the repository root is the working directory.

Example (supported by the repository):
```bash
pip install -r requirements.txt
```

### 15.2 Data setup
The project expects data in:
- data/raw/
- data/processed/

The verified catalog file is already present in the repository under data/raw/verified_product_catalog_2025_2026.csv.

### 15.3 Running Python scripts
Supported run commands explicitly present in the repository:

```bash
python src/data_processing.py
```
This generates processed data outputs and validation results.

```bash
python src/run_sql_pipeline.py
```
This executes the SQL warehouse pipeline and writes the data/processed/sql outputs.

```bash
python src/generate_excel_workbook.py
```
This generates outputs/Market_Business_Strategy_Intelligence.xlsx.

```bash
python quick_verify.py
```
This runs the pytest suite.

### 15.4 Running notebooks
The project contains a notebook at prompt_3a_verification.ipynb. It can be opened in Jupyter or VS Code notebook support, but the repository state shows no executed outputs and no explicit final result file derived from the notebook.

### 15.5 Running SQL
The SQL scripts under sql/ are designed to be run by the Python launcher in src/run_sql_pipeline.py. The scripts are loaded in order:
1. 01_schema.sql
2. 02_load_verified_data.sql
3. 03_data_quality.sql
4. 04_competitive_analysis.sql
5. 05_pricing_analysis.sql
6. 06_product_positioning.sql
7. 07_kpi_queries.sql
8. 08_pending_market_queries.sql

### 15.6 Generating outputs
The outputs are produced by the scripts above:
- processed CSV files by Python and SQL
- Excel workbook by src/generate_excel_workbook.py
- Power BI project source files are already present; the repository does not provide a single command to open and render the report in Power BI Desktop

### 15.7 Dashboard-related steps
The repository includes Power BI project files, but no direct CLI command to open or refresh the dashboard is present. The repo instead contains the PBIP source and validation script. Power BI Desktop is the actual tool to open the project.

### 15.8 End-to-end run completeness
The repository supports a practical end-to-end run for verified product catalog analytics and dashboard preparation. It does not support a verified end-to-end run for national Vahan registration-based market sizing because the official registration datasets are absent and intentionally fail-closed.

---

## 16. Current Project Status

### 16.1 Completed components
The following components are present and operational as actual repository artifacts:
- verified product catalog ingestion and validation
- Python ETL and processing scripts
- SQL warehouse schema and marts
- KPI output generation
- Excel workbook generation
- Power BI project source files and model definitions
- validation and quality checks
- fail-closed framework for pending registration metrics

### 16.2 Partially completed components
- Geographic analysis and GAI templates are implemented structurally, but verified state-level input data is not available in the repo.
- Unit economics and scenario models are present as templates and assumptions, but they are not proven against a full official market dataset.
- Some detailed docs describe strategic workstreams that extend beyond the verified repo inputs and are therefore partially conceptual.

### 16.3 Planned components
- Official Vahan registration data ingestion and market-volume analysis
- State-level market-share and geographic ranking based on official registration data
- More complete upstream market-sizing and TAM/SAM/SOM calculations if authoritative inputs are later added

### 16.4 Placeholder components
- pending.market_queries_template in SQL
- geographic_scoring_template.csv
- strategic_priority_template.csv
- scenario_analysis_template.csv
- unit_economics_input_template.csv
- unit_economics_results.csv
- any KPI or metric marked as PENDING VERIFIED DATA

### 16.5 Known issues
Confirmed from repository evidence:
- The repository does not contain official Vahan registration data, so registration-based market metrics remain pending.
- The notebook is unexecuted in the current workspace state.
- Some raw datasets in data/raw/ are clearly labeled as generated_proxy or manual_compilation_unverified; they are retained only for governance and demonstration purposes.
- The exact full Power BI rendered report cannot be directly opened and checked in this environment from repository state alone.

### 16.6 Missing pieces
The repository is missing actual official market registration data and a complete set of authoritative state-level EV market time series. This is explicitly documented as a known limitation.

### 16.7 Technical limitations
- No live external API integration is implemented in the repo.
- No production-grade deployment process is defined.
- The project relies on local files rather than a scheduled pipeline or database service.

---

## 17. Existing Documentation

The repository contains several documents that describe the project in different ways. The main ones are:

### 17.1 README.md
This document presents the project as a verified commercial strategy and competitive intelligence platform for the Indian electric two-wheeler market. It emphasizes that the project is not using unverified registration data and that it is a strict, provenance-aware repository.

### 17.2 implementation_plan.md
This is the strategic blueprint. It defines the market-entry and strategic planning scenario, the key analytical questions, and the expected workstreams around market sizing, competitive analysis, pricing, geographic attractiveness, scenario analysis, and strategic prioritization.

### 17.3 CONTEXT.md
This file is intended to provide a repository-level technical context. The current version is repository-grounded and separates verified facts from pending or template-based elements.

### 17.4 docs/ files
The docs are extensive and cover:
- KPI theory and registry
- data source register and provenance audit
- Power BI DAX, model, and query definitions
- SQL analytics and product positioning
- strategic analysis and market entry frameworks
- geographic and unit economics frameworks

### 17.5 Documentation consistency check
The repository documentation is broadly consistent on the core fact that:
- verified product catalog data is the primary factual layer
- Vahan-based market-share and registration analytics are intentionally pending
- the project avoids proxy or fabricated registration claims

The main contradiction to watch for is that some earlier planning and historical documentation refers to more expansive market-size or Vahan-driven workstreams, while the current implemented repo intentionally keeps those metrics fail-closed because the required data is absent.

---

## 18. Important Relationships

### 18.1 Data → SQL
- Verified product catalog CSV is loaded into stg_verified_products in 02_load_verified_data.sql.
- Raw/proxy datasets remain quarantined and are not treated as observed analytics.

### 18.2 SQL → Python
- Python scripts run the SQL pipeline and consume its outputs.
- Python also validates the quality of the raw and processed datasets before SQL reads them.

### 18.3 Python → outputs
- Python processing writes the processed CSV files and generated workbook.
- The processed files serve as data inputs for downstream Excel and Power BI consumption.

### 18.4 Data → Power BI
- Power BI uses processed CSV marts, especially data/processed/sql/*.csv, as the source for semantic-model tables and DAX measures.
- The report definitions and semantic model are in the repository and are reconciled to the output data.

### 18.5 SQL metrics → dashboard metrics
- The SQL marts become the dashboard’s fact and dimension tables.
- KPI results from sql_kpi_results.csv directly map to the Power BI display metrics.
- Price, range, and positioning views drive the dashboard visuals.

### 18.6 Notebooks → final outputs
- The notebook is present but currently unexecuted, and no final artifact derived from it is shown in the repository state.
- The final outputs come primarily from the Python and SQL pipeline rather than the notebook itself.

### 18.7 Verification scripts → project results
- Validation scripts confirm data integrity and model structure.
- The project exposes a chain of evidence: raw manifest → processed validation → SQL quality checks → data marts → Excel workbook → Power BI model.

---

## 19. Known Issues / Risks / Limitations

### 19.1 Confirmed issues
- Official Vahan registration data is not present in the repository. This blocks actual market volume, growth, and OEM market-share analysis from being treated as verified industry data.
- Historical data sources for market registration are documented as proxy, pending, or non-eligible in the manifest.
- Some raw datasets are intentionally not used for factual analytics because they are legacy or generated proxies.
- The notebook is not executed in the current state, so notebook-based validation output is not available from the workspace.

### 19.2 Potential concerns
- Some documentation refers to analytical workstreams that would require more comprehensive and official datasets than are in the repository.
- The repo’s models and templates are designed to accommodate future data, but they are not a substitute for actual verified market registrations.
- Power BI inspection is limited to source files; the compiled report itself was not directly opened in this environment.

### 19.3 Data quality notes
The project explicitly treats missing values and unsupported fields as part of the data source reality, especially for pricing and technical fields where not all brands publish all values. This is handled through blanks and provenance tagging rather than synthetic imputation.

### 19.4 Reproducibility and dependency notes
- The project is local-file based and not a cloud pipeline.
- It depends on local installation of Python and required packages.
- It relies on accurate repository state and file paths under the repo root.

---

## 20. Improvement Opportunities

### 20.1 Architecture
- Formalize a single source-of-truth project workflow document covering exact ETL, SQL, and Power BI execution order.
- Add a standardized orchestrator script for dependency chaining and run order.

### 20.2 Code quality
- Add stronger unit tests around SQL output shapes and schema expectations.
- Clean up overlapping and duplicated analytical functions across modules.

### 20.3 Data engineering
- Add a more explicit ingest workflow for future official Vahan data when it becomes available.
- Standardize the handling of missing or location-specific pricing values across all product sources.

### 20.4 SQL
- Add explicit schema versioning and migration notes.
- Add more explicit tests for each SQL mart output.

### 20.5 Analytics
- Add a clear distinction between verified product metrics and scenario-based metrics in all docs and dashboards.
- Expand explanatory notes on how HHI, price buckets, and product positioning are computed.

### 20.6 Business intelligence
- Add a data dictionary view in the Power BI model for all calculated fields and measures.
- Add explicit documentation for slicers, page-level filters, and field mappings.

### 20.7 Power BI
- Include a more explicit validation procedure for each page and measure in the model.
- Add direct reports or screenshots if they are intended as project deliverables for stakeholders.

### 20.8 Testing
- Add end-to-end tests that verify output CSV schemas and row counts against expectations.
- Include notebook execution status as part of repository validation.

### 20.9 Documentation
- Consolidate occasionally overlapping docs to reduce drift between plan-level and implementation-level narratives.
- Add a single “current-state reality” summary for verified vs pending work.

### 20.10 Reproducibility
- Add environment lock files or explicit version pinning for all runtime dependencies beyond requirements.txt.
- Add a reproducible README command sequence for full project execution from a clean machine.

### 20.11 Performance
- Add database-level performance checks for large datasets when additional market data is ingested.
- Reduce unnecessary duplicate data passes in the Python pipeline.

### 20.12 Security
- Keep secrets, tokens, and credentials out of repo files; the current repo appears to respect that, but future environment config should remain secret-safe.

### 20.13 User experience
- Add a clearer project landing page that distinguishes verified outputs from pending templates and strategic scenarios.

---

## 21. AI Handoff Summary

This repository is a verified product-intelligence and strategy-analysis project for the Indian electric two-wheeler market. Its current architecture is a local Python + SQL + Power BI pipeline that validates product-level OEM data, calculates price/range/product-positioning metrics, and produces a Power BI dashboard and Excel workbook. The repository intentionally refuses to present unverified or proxy Vahan registration data as fact; instead, it keeps registration-based growth and market-share work explicit templates with fail-closed safeguards.

Main technologies:
- Python
- pandas, numpy, xlsxwriter, duckdb, pytest
- DuckDB SQL
- Power BI PBIP + DAX + Power Query
- Excel workbook generation

Main datasets:
- verified_product_catalog_2025_2026.csv
- processed_verified_product_catalog.csv
- SQL marts under data/processed/sql/
- raw legacy/proxy files retained only for provenance review

Main analyses:
- competitive comparison across manufacturers and models
- pricing and value analysis
- product positioning and whitespace analysis
- KPI registry and HHI calculation
- geographic attractiveness template
- unit economics and scenario modeling templates

Important KPIs currently supported by the repo:
- manufacturer_count = 11
- product_count = 42
- priced_product_count = 34
- average_price_inr = 136349.21
- median_price_inr = 126170.5
- average_range_km = 159.39
- average_battery_kwh = 3.73
- average_price_per_km = 867.71
- product_portfolio_hhi = 1326.53

Current status:
- verified product catalog analytics are complete and operational
- SQL marts and Power BI project files exist
- official Vahan market-registration analytics remain pending and fail-closed

Important files:
- README.md
- requirements.txt
- data/raw/DATASET_MANIFEST.csv
- data/processed/validation_results.json
- sql/01_schema.sql through sql/08_pending_market_queries.sql
- src/data_processing.py
- src/run_sql_pipeline.py
- src/generate_excel_workbook.py
- powerbi/validate_pbip.py
- outputs/Market_Business_Strategy_Intelligence.xlsx

Known issues:
- no official Vahan registration dataset in the repo
- unverified legacy datasets are retained only as quarantined references
- notebook execution state is not complete in this workspace
- some docs describe more complete market workstreams than can be fully verified from repository data alone

Potential improvement areas:
- formalize full end-to-end orchestration
- strengthen end-to-end tests and SQL schema checks
- add official Vahan ingestion once accessible
- clarify the distinction between verified outputs and scenario/pending templates in dashboards and docs

Important note for any AI making changes:
- do not treat legacy or proxy datasets as factual market data
- do not fabricate market-share or registration metrics absent an official dataset
- keep the project’s provenance-first and fail-closed logic intact
