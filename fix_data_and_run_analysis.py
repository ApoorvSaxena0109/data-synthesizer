#!/usr/bin/env python3
"""
FIX DATA PIPELINE AND RUN CORRECTED ANALYSIS
=============================================
This script fixes the critical data issue where AFFECTED_RATIO was all zeros
in the company_year_panel_with_affected_ratio.parquet file.

The fix: Re-aggregate disaster exposure from facility-level data where it exists.

Run this in Google Colab BEFORE running notebooks 7 or 8.

Author: Data Pipeline Fix
Date: December 2025
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("DATA PIPELINE FIX - Hsu et al. (2018) Replication")
print("=" * 80)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# ============================================================================
# CONFIGURATION - Update these paths for your environment
# ============================================================================
# For Google Colab:
BASE_PATH = Path('/content/drive/MyDrive/Paper1_Dataset')
PROCESSED_PATH = BASE_PATH / 'processed'

# ============================================================================
# STEP 1: Load facility-level data (has correct disaster exposure)
# ============================================================================
print("\n" + "=" * 80)
print("STEP 1: LOADING FACILITY-LEVEL DATA")
print("=" * 80)

facility_data = pd.read_parquet(PROCESSED_PATH / 'analysis_dataset_complete.parquet')
print(f"Facility data loaded: {len(facility_data):,} rows")
print(f"  With PERMNO: {facility_data['PERMNO'].notna().sum():,}")
print(f"  With disasters: {(facility_data['num_disasters'] > 0).sum():,}")
print(f"  disaster_exposed sum: {facility_data['disaster_exposed'].sum():,}")

# ============================================================================
# STEP 2: Aggregate to company-year level (with correct disaster exposure)
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: AGGREGATING TO COMPANY-YEAR LEVEL")
print("=" * 80)

# Keep only matched facilities
matched = facility_data[facility_data['PERMNO'].notna()].copy()
print(f"Matched facility-years: {len(matched):,}")

# Aggregate to company-year
company_year = matched.groupby(['PERMNO', 'DATA_YEAR']).agg({
    'TRIFD': 'count',
    'num_disasters': 'sum',
    'disaster_exposed': 'sum',
    'TICKER': 'first'
}).reset_index()

company_year.columns = ['PERMNO', 'YEAR', 'total_facilities', 'num_disasters',
                        'exposed_facilities', 'TICKER']

# Calculate AFFECTED_RATIO correctly
company_year['AFFECTED_RATIO'] = company_year['exposed_facilities'] / company_year['total_facilities']
company_year['DISASTER'] = (company_year['exposed_facilities'] > 0).astype(int)

print(f"Company-year panel created: {len(company_year):,} rows")
print(f"  Unique companies: {company_year['PERMNO'].nunique():,}")
print(f"  Years: {company_year['YEAR'].min()}-{company_year['YEAR'].max()}")
print(f"  AFFECTED_RATIO mean: {company_year['AFFECTED_RATIO'].mean():.4f}")
print(f"  % with exposure > 0: {(company_year['AFFECTED_RATIO'] > 0).mean()*100:.1f}%")

# ============================================================================
# STEP 3: Load financial data from old file
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: LOADING FINANCIAL DATA")
print("=" * 80)

old_file = pd.read_parquet(PROCESSED_PATH / 'company_year_panel_with_affected_ratio.parquet')
financial_cols = ['PERMNO', 'YEAR', 'TOTAL_ASSETS', 'TOTAL_DEBT', 'NET_INCOME',
                  'TOTAL_REVENUE', 'CASH_FROM_OPS', 'CAPITAL_EXPENDITURE']
financial = old_file[financial_cols].copy()
print(f"Financial data loaded: {len(financial):,} rows")

# ============================================================================
# STEP 4: Merge correctly
# ============================================================================
print("\n" + "=" * 80)
print("STEP 4: MERGING DATA")
print("=" * 80)

merged = company_year.merge(financial, on=['PERMNO', 'YEAR'], how='inner')
print(f"Merged data: {len(merged):,} rows")
print(f"  Unique companies: {merged['PERMNO'].nunique():,}")
print(f"  Years: {merged['YEAR'].min()}-{merged['YEAR'].max()}")

# ============================================================================
# STEP 5: Create variables per Hsu et al. (2018)
# ============================================================================
print("\n" + "=" * 80)
print("STEP 5: CREATING VARIABLES (Hsu et al. 2018 Specification)")
print("=" * 80)

# Sort by company and year
merged = merged.sort_values(['PERMNO', 'YEAR']).reset_index(drop=True)

# Create LAGGED variables
merged['AFFECTED_RATIO_lag1'] = merged.groupby('PERMNO')['AFFECTED_RATIO'].shift(1)
merged['TOTAL_ASSETS_lag1'] = merged.groupby('PERMNO')['TOTAL_ASSETS'].shift(1)

# Calculate ROA with lagged assets (Hsu et al. specification)
merged['ROA'] = merged['NET_INCOME'] / merged['TOTAL_ASSETS_lag1']

# Also keep contemporaneous ROA for comparison
merged['ROA_contemporaneous'] = merged['NET_INCOME'] / merged['TOTAL_ASSETS']

# Control variables
merged['LOG_ASSETS'] = np.log(merged['TOTAL_ASSETS'] + 1)
merged['LEVERAGE'] = merged['TOTAL_DEBT'] / merged['TOTAL_ASSETS']

# Additional variables
merged['ROA_lag1'] = merged.groupby('PERMNO')['ROA'].shift(1)
merged['ROA_lead1'] = merged.groupby('PERMNO')['ROA'].shift(-1)
merged['DELTA_ROA'] = merged['ROA'] - merged['ROA_lag1']
merged['ASSET_GROWTH'] = merged.groupby('PERMNO')['TOTAL_ASSETS'].pct_change()

print("Variables created:")
print(f"  AFFECTED_RATIO mean: {merged['AFFECTED_RATIO'].mean():.4f}")
print(f"  AFFECTED_RATIO_lag1 mean: {merged['AFFECTED_RATIO_lag1'].mean():.4f}")
print(f"  ROA (lagged assets) mean: {merged['ROA'].mean():.4f}")
print(f"  ROA (contemporaneous) mean: {merged['ROA_contemporaneous'].mean():.4f}")
print(f"  Hsu et al. ROA mean: ~0.16")

# ============================================================================
# STEP 6: Save corrected file
# ============================================================================
print("\n" + "=" * 80)
print("STEP 6: SAVING CORRECTED FILE")
print("=" * 80)

output_file = PROCESSED_PATH / 'company_year_panel_with_affected_ratio.parquet'
merged.to_parquet(output_file, index=False)
print(f"Saved: {output_file}")

# Verify
check = pd.read_parquet(output_file)
print(f"\nVerification:")
print(f"  Rows: {len(check):,}")
print(f"  AFFECTED_RATIO mean: {check['AFFECTED_RATIO'].mean():.4f}")
print(f"  AFFECTED_RATIO max: {check['AFFECTED_RATIO'].max():.4f}")
print(f"  % with exposure > 0: {(check['AFFECTED_RATIO'] > 0).mean()*100:.1f}%")

# ============================================================================
# STEP 7: Run regressions (Hsu et al. 2018 specification)
# ============================================================================
print("\n" + "=" * 80)
print("STEP 7: RUNNING REGRESSIONS (Hsu et al. 2018)")
print("=" * 80)

# Prepare regression data - exclude 2022-2023 (no disaster data)
reg_data = merged.dropna(subset=['ROA', 'AFFECTED_RATIO_lag1', 'LOG_ASSETS', 'LEVERAGE'])
reg_data = reg_data[reg_data['YEAR'] <= 2021]

print(f"\nRegression sample:")
print(f"  Observations: {len(reg_data):,}")
print(f"  Companies: {reg_data['PERMNO'].nunique():,}")
print(f"  Years: {reg_data['YEAR'].min()}-{reg_data['YEAR'].max()}")

# Check correlation
corr = reg_data[['ROA', 'AFFECTED_RATIO_lag1']].corr().iloc[0,1]
print(f"\nCorrelation (ROA vs AFFECTED_RATIO_lag1): {corr:.4f}")

# Model 1: Simple OLS with LAGGED exposure
print("\n" + "-" * 80)
print("MODEL 1: Simple OLS (Lagged Exposure)")
print("-" * 80)
model1 = smf.ols('ROA ~ AFFECTED_RATIO_lag1', data=reg_data).fit()
print(f"  β(AFFECTED_RATIO_lag1) = {model1.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  Std Error = {model1.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value = {model1.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R² = {model1.rsquared:.4f}")

# Model 2: With Controls
print("\n" + "-" * 80)
print("MODEL 2: With Firm Controls")
print("-" * 80)
model2 = smf.ols('ROA ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE', data=reg_data).fit()
print(f"  β(AFFECTED_RATIO_lag1) = {model2.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  Std Error = {model2.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value = {model2.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R² = {model2.rsquared:.4f}")

# Model 3: With Year Fixed Effects
print("\n" + "-" * 80)
print("MODEL 3: With Year Fixed Effects")
print("-" * 80)
model3 = smf.ols('ROA ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + C(YEAR)',
                 data=reg_data).fit()
print(f"  β(AFFECTED_RATIO_lag1) = {model3.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  Std Error = {model3.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value = {model3.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R² = {model3.rsquared:.4f}")

# Model 4: With Firm Fixed Effects (Hsu et al. full specification)
print("\n" + "-" * 80)
print("MODEL 4: With Year + Firm Fixed Effects (Hsu et al. Specification)")
print("-" * 80)
model4 = smf.ols('ROA ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + C(YEAR) + C(PERMNO)',
                 data=reg_data).fit()
print(f"  β(AFFECTED_RATIO_lag1) = {model4.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  Std Error = {model4.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value = {model4.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R² = {model4.rsquared:.4f}")

# ============================================================================
# STEP 8: Summary and Comparison
# ============================================================================
print("\n" + "=" * 80)
print("RESULTS SUMMARY")
print("=" * 80)

print(f"""
┌────────────────────────────────────────────────────────────────────────────┐
│                    REGRESSION RESULTS COMPARISON                            │
├────────────────────────────────────────────────────────────────────────────┤
│ Model                          │ Coefficient │ Std Error │ P-value │ R²    │
├────────────────────────────────┼─────────────┼───────────┼─────────┼───────┤
│ Model 1: Simple OLS            │ {model1.params['AFFECTED_RATIO_lag1']:11.6f} │ {model1.bse['AFFECTED_RATIO_lag1']:9.6f} │ {model1.pvalues['AFFECTED_RATIO_lag1']:7.4f} │ {model1.rsquared:.4f} │
│ Model 2: With Controls         │ {model2.params['AFFECTED_RATIO_lag1']:11.6f} │ {model2.bse['AFFECTED_RATIO_lag1']:9.6f} │ {model2.pvalues['AFFECTED_RATIO_lag1']:7.4f} │ {model2.rsquared:.4f} │
│ Model 3: Year FE               │ {model3.params['AFFECTED_RATIO_lag1']:11.6f} │ {model3.bse['AFFECTED_RATIO_lag1']:9.6f} │ {model3.pvalues['AFFECTED_RATIO_lag1']:7.4f} │ {model3.rsquared:.4f} │
│ Model 4: Year + Firm FE        │ {model4.params['AFFECTED_RATIO_lag1']:11.6f} │ {model4.bse['AFFECTED_RATIO_lag1']:9.6f} │ {model4.pvalues['AFFECTED_RATIO_lag1']:7.4f} │ {model4.rsquared:.4f} │
├────────────────────────────────┼─────────────┼───────────┼─────────┼───────┤
│ Hsu et al. (2018) Table 3      │    -0.012   │   0.004   │  <0.01  │  --   │
└────────────────────────────────┴─────────────┴───────────┴─────────┴───────┘

Sample: N={len(reg_data):,} firm-years, {reg_data['PERMNO'].nunique()} firms, {reg_data['YEAR'].min()}-{reg_data['YEAR'].max()}
""")

# Interpretation
coef4 = model4.params['AFFECTED_RATIO_lag1']
pval4 = model4.pvalues['AFFECTED_RATIO_lag1']

print("=" * 80)
print("INTERPRETATION")
print("=" * 80)

if coef4 < 0:
    print(f"✓ Coefficient is NEGATIVE ({coef4:.6f})")
    print(f"  → 100% disaster exposure → {abs(coef4)*100:.2f}% ROA decline")
else:
    print(f"✗ Coefficient is POSITIVE ({coef4:.6f})")

if pval4 < 0.01:
    print(f"✓ SIGNIFICANT at 1% level (p={pval4:.4f})")
elif pval4 < 0.05:
    print(f"✓ SIGNIFICANT at 5% level (p={pval4:.4f})")
elif pval4 < 0.10:
    print(f"~ Marginally significant at 10% level (p={pval4:.4f})")
else:
    print(f"✗ NOT SIGNIFICANT (p={pval4:.4f})")

print(f"""
NOTES:
- Results may differ from Hsu et al. (2018) due to:
  1. Different time period: 2016-2021 vs 1987-2014
  2. Using Net Income instead of OIBDP (Operating Income Before Depreciation)
  3. Smaller sample size: ~{len(reg_data):,} vs 16,709 observations
  4. Different disaster definition: All SHELDUS vs major only (>$1B)

- Modern manufacturing firms (2016-2021) may be more resilient due to:
  1. Better insurance coverage
  2. More diversified supply chains
  3. Improved disaster preparedness
  4. Technology improvements
""")

print("=" * 80)
print("DATA PIPELINE FIX COMPLETE!")
print("=" * 80)
print(f"""
The corrected file has been saved to:
  {output_file}

You can now run Notebooks 7 or 8 to generate final outputs.
The AFFECTED_RATIO variable is now correctly populated.
""")
