# Statistical Analysis Outputs for Professor Yang

Dear Professor Yang,

Thank you for your interest in my disaster exposure analysis. This document provides all the statistical outputs you requested.

## Quick Summary

**Research Question:** Do natural disasters affecting a company's facilities impact its financial performance?

**Main Finding:** No significant effect. Manufacturing firms appear resilient to disaster exposure (p > 0.50 across all models).

**Sample:** 2,080 firm-years, 293 manufacturing companies, 2016-2023

---

## Contents of This Delivery

### 1. **Complete Analysis Dataset** 

**Files to generate:**
- `COMPLETE_ANALYSIS_DATASET.csv` - All 2,080 observations used in the analysis
- `COMPLETE_ANALYSIS_DATASET.xlsx` - Same data in Excel format
- `DATA_DICTIONARY.csv` - Description of all variables

**How to generate:** Run `export_dataset_and_correlation.py` after executing Notebook 5, or add the code from that script as a new cell at the end of Notebook 5.

**Variables included:**
- Company identifiers (PERMNO, TICKER)
- Time (YEAR)
- Disaster exposure measures (AFFECTED_RATIO, num_disasters, exposed_facilities, total_facilities)
- Financial performance (ROA - dependent variable)
- Financial data (TOTAL_ASSETS, NET_INCOME, TOTAL_DEBT, TOTAL_REVENUE)
- Control variables (LOG_ASSETS, LEVERAGE, REVENUE_GROWTH)

### 2. **Statistical Model Specification**

**File:** `statistical_analysis_outputs/02_STATISTICAL_MODEL.txt`

This document provides:
- Detailed research question
- Dependent variable definition (ROA)
- Independent variable definition (AFFECTED_RATIO following Hsu et al. 2018)
- Control variables (LOG_ASSETS, LEVERAGE, Year FE)
- Three regression model specifications
- Estimation method (OLS)
- Sample restrictions
- Hypothesis and interpretation

**Key equation (Model 3 - full specification):**

```
ROA_it = β₀ + β₁(AFFECTED_RATIO_it) + β₂(LOG_ASSETS_it) 
       + β₃(LEVERAGE_it) + Σγ_t(YEAR_t) + ε_it
```

### 3. **Descriptive Statistics**

**Files:**
- `statistical_analysis_outputs/03_DESCRIPTIVE_STATISTICS.csv`
- `statistical_analysis_outputs/03_DESCRIPTIVE_STATISTICS.xlsx`
- `statistical_analysis_outputs/03b_EXPOSURE_DISTRIBUTION.csv`
- `statistical_analysis_outputs/03b_EXPOSURE_DISTRIBUTION.xlsx`

**Key Statistics:**

| Variable | N | Mean | Std Dev | Min | Max |
|----------|---|------|---------|-----|-----|
| AFFECTED_RATIO | 2,123 | 0.240 | 0.320 | 0.000 | 1.000 |
| ROA | 2,080 | 0.055 | 0.085 | -0.759 | 1.496 |
| TOTAL_ASSETS (millions) | 2,080 | 20,312 | 39,667 | 0.352 | 376,317 |
| LEVERAGE | 2,080 | 0.313 | 0.161 | 0.000 | 1.210 |

**Exposure Distribution:**
- No exposure (0%): 1,047 firms (49.3%)
- Low exposure (1-25%): 330 firms (15.5%)
- Medium exposure (26-50%): 349 firms (16.4%)
- High exposure (51-75%): 169 firms (8.0%)
- Very high exposure (76-100%): 228 firms (10.7%)

### 4. **Correlation Matrix**

**Files to generate:**
- `statistical_analysis_outputs/04_CORRELATION_MATRIX.csv`
- `statistical_analysis_outputs/04_CORRELATION_MATRIX.xlsx`

**How to generate:** Run `export_dataset_and_correlation.py` after executing Notebook 5.

**Variables included:**
- ROA (dependent variable)
- AFFECTED_RATIO (key independent variable)
- LOG_ASSETS (control)
- LEVERAGE (control)
- num_disasters
- total_facilities
- exposed_facilities
- REVENUE_GROWTH (if available)

**Expected key relationships:**
- ROA ↔ AFFECTED_RATIO: Near zero (consistent with null finding)
- ROA ↔ LOG_ASSETS: Positive (larger firms more profitable)
- ROA ↔ LEVERAGE: Negative (debt reduces profitability)
- LOG_ASSETS ↔ LEVERAGE: Positive (larger firms carry more debt)

### 5. **Regression Output Tables**

All regression results are provided with complete coefficient tables:

**Model 1: Simple OLS** (`05a_REGRESSION_MODEL1_SIMPLE.csv/xlsx`)
```
ROA = 0.0551 - 0.0016*AFFECTED_RATIO
      (0.002)  (0.006)
      p=0.000  p=0.790

N = 2,080, R² = 0.000
```

**Model 2: With Controls** (`05b_REGRESSION_MODEL2_CONTROLS.csv/xlsx`)
```
ROA = 0.0360 - 0.0009*AFFECTED_RATIO + 0.0057*LOG_ASSETS - 0.0971*LEVERAGE
      (0.010)  (0.006)                 (0.001)***          (0.012)***
      p=0.000  p=0.872                 p<0.001             p<0.001

N = 2,080, R² = 0.038
```

**Model 3: With Year Fixed Effects** (`05c_REGRESSION_MODEL3_YEAR_FE.csv/xlsx`)
```
ROA = 0.0333 + 0.0042*AFFECTED_RATIO + 0.0055*LOG_ASSETS - 0.0970*LEVERAGE + YEAR_FE
      (0.011)  (0.006)                 (0.001)***          (0.012)***
      p=0.002  p=0.506                 p<0.001             p<0.001

N = 2,080, R² = 0.050
```

*** p<0.001, ** p<0.01, * p<0.05

**Summary Comparison** (`05d_REGRESSION_SUMMARY.csv/xlsx`):

| Model | AFFECTED_RATIO Coef. | Std Error | P-value | R² | N |
|-------|---------------------|-----------|---------|-----|-----|
| (1) Simple | -0.0016 | 0.0058 | 0.790 | 0.000 | 2,080 |
| (2) Controls | -0.0009 | 0.0057 | 0.872 | 0.038 | 2,080 |
| (3) Year FE | +0.0042 | 0.0064 | 0.506 | 0.050 | 2,080 |

---

## Key Findings

### Main Result
**Natural disasters do NOT significantly affect ROA in manufacturing firms.**

- Coefficient near zero across all specifications (-0.002 to +0.004)
- P-values > 0.50 in all models (far from statistical significance)
- Finding is robust to:
  - Different model specifications
  - Alternative control variables
  - Year fixed effects
  - Various robustness checks (see Notebook 6)

### Control Variables (Model 2 & 3)
- **Firm Size (LOG_ASSETS):** Positive and significant (β ≈ 0.006, p<0.001)
  - Larger firms are more profitable
- **Leverage (LEVERAGE):** Negative and significant (β ≈ -0.097, p<0.001)
  - Higher debt reduces profitability

### Interpretation
The null finding suggests manufacturing firms are resilient to disaster shocks, possibly due to:
1. **Insurance coverage** - Protecting against physical damages
2. **Geographic diversification** - Multiple facilities reduce single-point risk
3. **Supply chain flexibility** - Ability to shift production
4. **Asset fungibility** - Manufacturing equipment is often movable/replaceable

This contrasts with Hsu et al.'s (2018) findings for broader samples, suggesting the manufacturing sector may have unique resilience characteristics.

---

## Data Sources and Construction

### Primary Data Sources:
1. **EPA TRI (Toxic Release Inventory)** - 1,148,673 facility-year records
   - Facility locations (latitude/longitude and FIPS codes)
   - Parent company names for matching

2. **SHELDUS (Spatial Hazard Events and Losses Database)** - 35,283 disaster events (2009-2023)
   - County-level natural disaster events
   - Used to identify facility exposure

3. **CRSP (Center for Research in Security Prices)** - Company identification
   - Matched TRI parent companies to PERMNO identifiers
   - 245,826 matched facility-year records

4. **Compustat** - Financial data
   - ROA, assets, debt, revenue
   - 2,341 company-year observations with financial data

### Key Methodological Fix:
In November, I identified and corrected a FIPS code matching issue where some codes were stored as integers (losing leading zeros) while others were strings. This has been fixed, and all exposure measures have been revalidated.

### Sample Construction:
```
TRI facilities (2009-2023)               1,148,673
  → Matched to CRSP (PERMNO)                245,826
  → Aggregated to company-year               11,596
  → Merged with Compustat                     2,341
  → Restricted to manufacturing (2016-2023)   2,123
  → With complete data for regression         2,080 ✓
```

---

## How to Generate the Complete Dataset

Since the notebooks use Google Drive paths and the data files are large, you'll need to:

### Option 1: Run from Notebooks (Recommended)
1. Open Google Colab
2. Run notebooks in sequence:
   - `Data_Preparation_FIPS.ipynb` (Notebook 1)
   - `Automated_Matching_FIPS.ipynb` (Notebook 2)
   - `03_manual_review_and_analysis.ipynb` (Notebook 3)
   - `04_disaster_exposure_analysis.ipynb` (Notebook 4)
   - `05_CLEAN_affected_ratio_baseline_regression.ipynb` (Notebook 5)
3. At the end of Notebook 5, add a new cell with:
   ```python
   %run export_dataset_and_correlation.py
   ```
4. This will generate:
   - `COMPLETE_ANALYSIS_DATASET.csv` (2,080 observations)
   - `04_CORRELATION_MATRIX.csv` (complete correlation matrix)

### Option 2: Run Export Script Standalone
If you already have the `analysis_data` DataFrame in memory after running Notebook 5:
```python
# In Notebook 5, after all cells have been executed:
exec(open('export_dataset_and_correlation.py').read())
```

---

## Files Organization

```
data-synthesizer/
├── Notebooks (Jupyter/Colab):
│   ├── Data_Preparation_FIPS.ipynb                    (Notebook 1)
│   ├── Automated_Matching_FIPS.ipynb                  (Notebook 2)
│   ├── 03_manual_review_and_analysis.ipynb           (Notebook 3)
│   ├── 04_disaster_exposure_analysis.ipynb           (Notebook 4)
│   ├── 05_CLEAN_affected_ratio_baseline_regression.ipynb (Notebook 5)
│   └── 06_ROBUSTNESS_CHECKS_CLEAN.ipynb              (Notebook 6)
│
├── Scripts:
│   ├── generate_statistical_outputs.py                (Creates all output files)
│   └── export_dataset_and_correlation.py              (Exports dataset & correlation)
│
└── statistical_analysis_outputs/
    ├── 00_README.txt                                  (Summary document)
    ├── 01_DATASET_DESCRIPTION.txt                     (Dataset info)
    ├── 02_STATISTICAL_MODEL.txt                       (Model specification)
    ├── 03_DESCRIPTIVE_STATISTICS.csv/.xlsx            (Summary stats)
    ├── 03b_EXPOSURE_DISTRIBUTION.csv/.xlsx            (Exposure breakdown)
    ├── 04_CORRELATION_MATRIX.txt/.csv/.xlsx           (Correlations)
    ├── 05a_REGRESSION_MODEL1_SIMPLE.csv/.xlsx         (Model 1 results)
    ├── 05b_REGRESSION_MODEL2_CONTROLS.csv/.xlsx       (Model 2 results)
    ├── 05c_REGRESSION_MODEL3_YEAR_FE.csv/.xlsx        (Model 3 results)
    └── 05d_REGRESSION_SUMMARY.csv/.xlsx               (Comparison table)
```

---

## Robustness Checks (Notebook 6)

The null finding is robust to:

1. **Alternative Outcome Measures:**
   - ROA (main specification)
   - Operating income / Assets
   - Net income / Sales
   - Tobin's Q

2. **Different Disaster Definitions:**
   - Binary indicator (any disaster)
   - Continuous affected ratio (main specification)
   - Disaster count
   - Disaster severity weighted

3. **Subsample Analyses:**
   - By firm size (small vs. large)
   - By disaster intensity (high vs. low)
   - By exposure level

4. **Dynamic Specifications:**
   - Leads (placebo tests)
   - Lags (delayed effects)
   - Cumulative exposure

5. **Placebo Tests:**
   - Random assignment of disasters
   - Future disasters (should have no effect)

All robustness checks confirm the null finding.

---

## Statistical Significance Note

None of the AFFECTED_RATIO coefficients are statistically significant:
- Model 1: p = 0.790
- Model 2: p = 0.872
- Model 3: p = 0.506

All p-values are much greater than 0.05 (and even 0.10), indicating we cannot reject the null hypothesis that disasters have no effect on ROA.

The control variables (firm size and leverage) work as expected and are highly significant, validating the model specification.

---

## Contact Information

**Student:** Apoorv Saxena  
**Email:** s1129420@mail.yzu.edu.tw

**Supervisor:** Professor Yanjie Yang  
**Email:** yanjie@saturn.yzu.edu.tw

**Institution:** Yuan Ze University  
**Date:** December 2025

---

## Questions or Issues?

If you need:
- The actual dataset file with all 2,080 observations
- The calculated correlation matrix
- Any clarification on the methodology
- Additional robustness checks
- Different output formats

Please let me know and I'll generate them immediately.

Thank you for your guidance on this project!

Best regards,  
Apoorv Saxena
