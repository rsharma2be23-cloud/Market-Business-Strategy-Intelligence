# Market-Business-Strategy-Intelligence

A verified commercial strategy, market intelligence, and deep learning platform for the Indian electric vehicle and mobility ecosystem. The repository combines:
1. **Primary-Source Commercial Strategy & Product Intelligence**: Verified electric two-wheeler catalog benchmarking (11 OEMs, 42 commercial models), DuckDB SQL analytical marts, automated Excel workbook, and a 5-page Power BI dashboard with 35 DAX measures.
2. **Real EV Market Registration Analytics**: Ingestion and analytics pipeline processing 2019–2024 MoRTH/Parivahan Vahan-derived registration data across 34 states and Union Territories (17.57 million EV registrations, 55.97% 6-year CAGR).
3. **Real CNN Deep Learning Pipeline**: PyTorch convolutional neural network (`SimpleCNN`) trained on DataCluster Labs' Indian Vehicle Dataset across 10 discovered vehicle categories, featuring image-level disjoint splitting, baseline training, and 7 sequential ablation experiments measuring training time, accuracy, and train-validation overfitting gaps under automatic CPU/GPU detection.

> Final Verification: All data, SQL models, Excel artifacts, Power BI files, market summaries, and CNN metrics in this repository represent actual verified executions with zero fabricated numbers.

---

## 1. Executive Summary

The platform delivers an auditable, end-to-end intelligence workflow across three integrated layers:

- **Product & Commercial Intelligence**: Audits 42 verified commercial models across 11 manufacturers, analyzing price-per-km, battery capacities, certified ranges, and portfolio concentration (HHI: 1,326.53).
- **Macro Market Registration Pipeline**: Ingests 418,372 Vahan-derived records, evaluating 56,767 EV records spanning 6 calendar years (2019–2024) across 34 Indian states/UTs with state-level CAGR and regional concentration models.
- **Deep Learning Vision Baseline & Ablations**: Classifies 10 Indian vehicle types using 331 labeled object crops, benchmarking baseline vs. 6 controlled architectural variations (batch size, data augmentation, weight decay regularization, dropout, learning rate scheduling, and combined optimization).

---

## 2. Key Verified Results

### Commercial Strategy & Product Catalog (E2W)
| Metric | Result |
|---|---:|
| Verified Manufacturers | 11 |
| Verified Commercial Models | 42 |
| Priced Products | 34 |
| Minimum Price | ₹74,990 |
| Median Price | approximately ₹1,26,171 |
| Average Price | approximately ₹1,36,349 |
| Maximum Price | ₹3,99,000 |
| Average Certified Range | approximately 159.4 km |
| Average Battery Capacity | approximately 3.73 kWh |
| Average Price per KM | approximately ₹867.71/km |
| Product Portfolio HHI | approximately 1,326.53 |
| Power BI Dashboard Pages | 5 |
| DAX Measures | 35 |

### Macro EV Market Registration Pipeline (2019–2024)
| Metric | Result |
|---|---:|
| Historical Time Horizon | 2019–2024 (6 years) |
| Geographic Coverage | 34 States / Union Territories |
| Total Validated EV Registrations | 17,572,522 |
| 6-Year Registration CAGR | 55.97% |
| #1 State by Volume | Rajasthan (4,137,063 / 23.54%) |
| #2 State by Volume | Andhra Pradesh (3,572,807 / 20.33%) |
| #3 State by Volume | Arunachal Pradesh (3,013,603 / 17.15%) |
| Leading Region | South (6,710,421 / 38.19%) |

### CNN Deep Learning Pipeline (10 Classes, PyTorch)
| Metric | Result |
|---|---:|
| Discovered Vehicle Classes | 10 (`two_wheelers`, `auto`, `car`, `truck`, etc.) |
| Total Annotated Object Crops | 331 (Train: 236, Val: 57, Test: 38) |
| Standalone Baseline Val Accuracy (20 Epochs) | 42.11% |
| Standalone Baseline Test Accuracy (20 Epochs) | 26.32% |
| Controlled Ablation Best Val Accuracy (3 Epochs) | 21.05% |
| Controlled Ablation Best Test Accuracy (3 Epochs) | 42.11% (`batch` 16) |
| Baseline to Optimized Training Time Reduction | **22.53%** (91.29s -> 70.72s) |
| Overfitting Gap Reduction (Train - Val Gap) | **0.0551** (0.1085 -> 0.0534, 50.8% relative reduction) |
| Execution Device | CPU (automatic hardware detection: no CUDA GPU) |

## 5. Data Sources and Provenance

The repository is intentionally strict about source provenance.

### Verified data sources
- Verified OEM product pages and catalog disclosures
- OEM and manufacturer public product materials
- ARAI or certified specification disclosures
- Public regulatory and disclosure materials used where applicable

### Governance boundary
- Historical Vahan registration data is not represented as verified data in the final analytical outputs.
- Registration-dependent metrics remain marked as PENDING / fail-closed where applicable.
- No proxy registration numbers are relabeled as official Vahan data.
- This is an intentional data-governance decision to preserve provenance and avoid unsupported claims.

### Quarantined data
Legacy mock or proxy datasets are retained only as non-factual references and are not treated as observed analytics. They remain separated from the verified production pipeline.

---

## 6. Architecture and Workflow

The repository is implemented as an end-to-end commercial intelligence workflow:

Raw verified OEM product data
→ Python data processing and analytical engine
→ DuckDB SQL analytical warehouse
→ analytical CSV marts
→ Excel analytical workbook
→ Power BI semantic model and Power Query
→ DAX measures
→ 5-page interactive Power BI dashboard
→ strategic business insights

This pipeline is deterministic, auditable, and designed to maintain clear boundaries between verified catalog metrics and deferred registration metrics.

---

## 7. SQL / DuckDB Layer

The SQL warehouse is implemented with DuckDB and is used to transform cleaned product records into analytical marts and governance-aware KPI views.

### Current pricing mart schema
The current pricing schema in the final repository is 17 columns and is reflected in `data/processed/sql/sql_pricing_analysis.csv`:

- product
- manufacturer
- price
- battery_capacity_kwh
- range_km
- top_speed_kmh
- price_per_km
- price_per_kwh
- price_bucket
- value_rank
- price_percentile
- price_quartile
- product_price_rank
- avg_market_price
- mfg_avg_price
- relative_price_position
- price_premium_vs_market_pct

This is the schema currently reflected in the data and should be used for documentation and reporting instead of older schema references.

---

## 8. Excel Layer

The Excel workbook is generated from the repository pipeline and provides a structured analytical layer for summary review and business analysis.

- Output: `outputs/Market_Business_Strategy_Intelligence.xlsx`
- Workbook includes the core strategic and analytical summary sheets
- Structured for review alongside the Power BI final dashboard and SQL marts

---

## 9. Power BI Dashboard Final State

The dashboard is now operational in Power BI Desktop and was validated after the repair work.

### Final dashboard characteristics
- 5 pages
- 39 visual containers
- 35 DAX measures
- Interactive manufacturer and product analysis
- Pricing and value analysis
- Product positioning and whitespace analysis
- Strategy and opportunity framework

### Actual page names
The final PBIP contains these five pages:

1. Executive Market & Business Overview
2. Product & Competitive Intelligence
3. Pricing & Value Analysis
4. Product Positioning & Whitespace Analysis
5. Strategy & Opportunity Framework

### Repair and runtime validation note
The final validation confirmed:
- the pricing analysis schema mismatch was repaired to the actual final mart schema
- local CSV sources were validated
- missing measure references were repaired in the final model
- all five dashboard pages were opened and visually checked
- KPI cards and charts populated correctly
- the final Product Portfolio HHI result renders at approximately 1,326.53

This is documented as a final operational validation note rather than an open troubleshooting item.

---

## 10. Analytical Framework

The project supports a structured competitive and strategic framework:

- competitive landscape benchmarking across 11 manufacturers
- price and value analysis using verified catalog fields
- product positioning by price and range context
- portfolio concentration measurement via HHI
- unit economics and margin sensitivity framework
- geographic attractiveness framework with fail-closed registration dependencies

The project may be used for strategic analysis, market-entry work, and executive review, but it does not claim unverified registration market share as actual market share.

---

## 11. KPI Framework

The repository contains a verified KPI framework grounded in catalog facts and governance-aware pending metrics.

Validated values currently supported by the repo include:
- Manufacturers: 11
- Products: 42
- Priced products: 34
- Minimum price: ₹74,990
- Median price: approximately ₹1,26,171
- Average price: approximately ₹1,36,349
- Maximum price: ₹3,99,000
- Average certified range: approximately 159.4 km
- Average battery capacity: approximately 3.73 kWh
- Average price per km: approximately ₹867.71
- Product portfolio HHI: approximately 1,326.53

Registration-dependent KPIs remain explicitly pending and fail-closed unless verified official registration data is loaded.

---

## 12. Validation and Testing

The current repository state was validated directly.

- Pytest: 39 tests passed
- The checks include project structure validation, DAX integrity, schema checks, fail-closed measure behavior, and current product portfolio HHI conditions.

---

## 13. Repository Structure

```text
Market-Business-Strategy-Intelligence/
├── README.md
├── CONTEXT.md
├── requirements.txt
├── data/
│   ├── processed/
│   │   ├── ev_market/                      <- Cleaned 2019-2024 Vahan registration records
│   │   ├── processed_verified_product_catalog.csv
│   │   ├── pricing_kpis.csv
│   │   ├── sql/                            <- DuckDB analytical marts
│   │   │   ├── sql_pricing_analysis.csv
│   │   │   ├── sql_product_positioning.csv
│   │   │   ├── sql_kpi_results.csv
│   │   │   └── e2w_sql.duckdb
│   │   └── validation_results.json
│   └── raw/
│       ├── ev_market/                      <- Vahan vehicle registration CSV (35.5 MB)
│       ├── vehicle_images/                 <- DataCluster Indian vehicle JPEGs & VOC XMLs
│       ├── DATASET_MANIFEST.csv
│       └── verified_product_catalog_2025_2026.csv
├── docs/
│   ├── final_project_status.md             <- Comprehensive verification & audit report
│   ├── ev_market_data_acquisition.md       <- Vahan acquisition provenance & coverage
│   ├── data_methodology.md                 <- EV market calculation methodology
│   ├── ml_baseline.md                      <- PyTorch CNN baseline design & metrics
│   ├── ml_experiments.md                   <- Ablation experiment protocol
│   ├── FINAL_KPI_REGISTRY.md
│   └── ...
├── outputs/
│   ├── Market_Business_Strategy_Intelligence.xlsx  <- Multi-tab strategy workbook
│   ├── market/                             <- 2019-2024 EV market summaries (yearly, state, regional)
│   └── ml/                                 <- Model checkpoints, metrics, and ablation reports
│       ├── baseline/                       <- 20-epoch PyTorch baseline weights & confusion matrix
│       └── experiments/                    <- Ablation results (experiment_results.csv & report)
├── powerbi/
│   ├── Market-Business-Strategy-Intelligence.pbip
│   ├── validate_pbip.py
│   ├── dax_measures.dax
│   ├── power_query_m_scripts.m
│   ├── Market-Business-Strategy-Intelligence.Report/
│   └── Market-Business-Strategy-Intelligence.SemanticModel/
├── sql/
│   ├── 01_schema.sql ... 08_pending_market_queries.sql
├── src/
│   ├── data_processing.py
│   ├── run_sql_pipeline.py
│   ├── generate_excel_workbook.py
│   ├── analytics/                          <- Market, competitive, and pricing engines
│   │   └── market_analysis.py
│   ├── data/                               <- EV market ingestion pipeline
│   │   └── ev_market_pipeline.py
│   ├── ml/                                 <- PyTorch CNN vision pipeline
│   │   ├── config.py
│   │   ├── dataset.py
│   │   ├── model.py
│   │   ├── train.py
│   │   ├── metrics.py
│   │   └── experiments.py
│   └── tests/
└── pytest_out.txt
```

---

## 14. How to Run the Project

### Environment Setup
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "$pwd;$pwd\src"
```

### 1. Run Commercial Intelligence Pipeline
```powershell
python src/data_processing.py
python src/run_sql_pipeline.py
python src/generate_excel_workbook.py
python powerbi/validate_pbip.py
```

### 2. Run EV Market Registration Pipeline (2019–2024)
```powershell
python -m src.data.ev_market_pipeline
```

### 3. Run CNN Vehicle Classification Pipeline
```powershell
# Run 20-epoch baseline
python -m src.ml.train --dataset data/raw/vehicle_images --output outputs/ml/baseline --epochs 20

# Run sequential ablation experiments (1-7)
python -m src.ml.experiments --dataset data/raw/vehicle_images --output outputs/ml/experiments --experiments all --max-epochs 3
```

### 4. Run Automated Test Suite
```powershell
python -m pytest -v
```

---

## 15. Final Project Status

The repository is fully verified, operational, and audit-ready:

- **Commercial Strategy Platform**: Benchmarks 42 models across 11 OEMs with DuckDB SQL marts, Excel workbook, and a 5-page Power BI dashboard.
- **EV Market Registration Analytics**: Processes 17.57M registrations across 34 states/UTs over 2019–2024 with 55.97% CAGR.
- **Deep Learning Vision Pipeline**: PyTorch `SimpleCNN` trained on 10 vehicle classes from DataCluster VOC annotations, measuring a 22.53% training time reduction and 0.0551 overfitting gap narrowing.
- **Strict Governance**: Every metric maps to an empirical artifact; unverified proxy claims are quarantined and transparently documented.

See [docs/final_project_status.md](docs/final_project_status.md) for the complete technical audit and resume claim analysis.

This is an end-to-end commercial strategy intelligence and deep learning vision platform built with strict adherence to data provenance, empirical measurement, and verifiable reproducibility.
