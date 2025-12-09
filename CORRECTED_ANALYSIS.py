#!/usr/bin/env python3
"""
CORRECTED ANALYSIS: Hsu et al. (2018) Replication
=================================================

This script implements the CORRECT methodology following Hsu et al. (2018).

Key Corrections:
1. LAGGED disaster exposure (t-1) instead of contemporaneous
2. ROA = OIBDP / lagged_Total_Assets (or approximation)
3. Firm fixed effects + Year fixed effects
4. Clustered standard errors (by state or firm)

Usage:
    python CORRECTED_ANALYSIS.py

Requirements:
    pip install pandas numpy statsmodels linearmodels

Author: Audit Correction Script
Date: December 2025
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("CORRECTED HSU ET AL. (2018) REPLICATION")
print("="*80)

# ============================================================================
# CONFIGURATION
# ============================================================================

# This script expects the following data files in the processed folder
# Adjust paths as needed for your environment
DATA_PATH = 'statistical_analysis_outputs/'  # or Google Drive path

# For demonstration, we'll create sample data structure
# In production, load from actual parquet/csv files

print("\n1. LOADING AND PREPARING DATA...")
print("-"*80)

# ============================================================================
# SAMPLE DATA STRUCTURE (Replace with actual data loading)
# ============================================================================

# Based on Notebook 5 output, the analysis dataset has these characteristics:
# - 2,080 firm-year observations
# - 292 unique companies
# - Years 2016-2023
# - Variables: PERMNO, YEAR, AFFECTED_RATIO, ROA, LOG_ASSETS, LEVERAGE, etc.

# Create sample data matching the structure
np.random.seed(42)

# In production, replace this with:
# data = pd.read_parquet('processed/analysis_dataset_complete.parquet')

# Demo data generation (replace with actual data)
n_companies = 292
n_years = 8
years = list(range(2016, 2024))

sample_data = []
for permno in range(10000, 10000 + n_companies):
    for year in years:
        sample_data.append({
            'PERMNO': permno,
            'YEAR': year,
            'AFFECTED_RATIO': np.random.beta(0.5, 2),  # Right-skewed like actual
            'TOTAL_ASSETS': np.exp(np.random.normal(8.7, 1.5)) * 1000,  # Log-normal
            'NET_INCOME': np.random.normal(500, 200),  # Can be negative
            'TOTAL_DEBT': np.random.uniform(0, 1) * np.exp(np.random.normal(8, 1.5)) * 1000,
            'OIBDP': np.random.normal(800, 300),  # Operating income before depreciation
            'STATE': np.random.choice(['TX', 'CA', 'OH', 'PA', 'IL', 'NY', 'FL', 'MI']),
        })

data = pd.DataFrame(sample_data)

print(f"✓ Loaded {len(data):,} observations")
print(f"✓ Unique companies: {data['PERMNO'].nunique()}")
print(f"✓ Years: {data['YEAR'].min()}-{data['YEAR'].max()}")

# ============================================================================
# STEP 1: CREATE LAGGED VARIABLES (CRITICAL FIX #1)
# ============================================================================

print("\n2. CREATING LAGGED VARIABLES...")
print("-"*80)

# Sort by company and year FIRST
data = data.sort_values(['PERMNO', 'YEAR'])

# Create lagged AFFECTED_RATIO (t-1)
# This is the CRITICAL fix - Hsu et al. use lagged disaster exposure
data['AFFECTED_RATIO_lag1'] = data.groupby('PERMNO')['AFFECTED_RATIO'].shift(1)

# Create lagged Total Assets for ROA denominator (t-1)
data['AT_lag1'] = data.groupby('PERMNO')['TOTAL_ASSETS'].shift(1)

# Also create second lag for robustness
data['AFFECTED_RATIO_lag2'] = data.groupby('PERMNO')['AFFECTED_RATIO'].shift(2)

print("✓ Created AFFECTED_RATIO_lag1 (lagged disaster exposure)")
print("✓ Created AT_lag1 (lagged total assets)")
print("✓ Created AFFECTED_RATIO_lag2 (for robustness)")

# Verify lagging is correct
print("\nVerification - Sample company time series:")
sample_company = data[data['PERMNO'] == 10000][['PERMNO', 'YEAR', 'AFFECTED_RATIO', 'AFFECTED_RATIO_lag1']].head(5)
print(sample_company.to_string(index=False))
print("  ↑ Note: 2016 has NaN for lag (no prior year data)")

# ============================================================================
# STEP 2: CALCULATE ROA CORRECTLY (CRITICAL FIX #2)
# ============================================================================

print("\n3. CALCULATING ROA USING HSU ET AL. DEFINITION...")
print("-"*80)

# Hsu et al. definition: ROA = OIBDP(t) / Total Assets(t-1)

# If OIBDP is available (preferred):
if 'OIBDP' in data.columns:
    data['ROA_HSU'] = data['OIBDP'] / data['AT_lag1']
    print("✓ ROA_HSU = OIBDP / lagged Total Assets (Hsu et al. exact definition)")
else:
    # Approximation using Net Income (less accurate)
    data['ROA_HSU'] = data['NET_INCOME'] / data['AT_lag1']
    print("⚠ ROA_HSU approximated using Net Income (OIBDP not available)")

# Also keep original ROA for comparison
data['ROA_ORIGINAL'] = data['NET_INCOME'] / data['TOTAL_ASSETS']

# Control variables
data['LOG_ASSETS'] = np.log(data['TOTAL_ASSETS'].replace(0, np.nan))
data['LEVERAGE'] = data['TOTAL_DEBT'] / data['TOTAL_ASSETS']

# Compare ROA measures
print(f"\nROA comparison:")
print(f"  Original (NI/AT):     Mean = {data['ROA_ORIGINAL'].mean():.4f}, Std = {data['ROA_ORIGINAL'].std():.4f}")
print(f"  Hsu et al. (OIBDP/lag AT): Mean = {data['ROA_HSU'].mean():.4f}, Std = {data['ROA_HSU'].std():.4f}")

# ============================================================================
# STEP 3: PREPARE REGRESSION SAMPLE
# ============================================================================

print("\n4. PREPARING REGRESSION SAMPLE...")
print("-"*80)

# Select regression variables
reg_vars = ['PERMNO', 'YEAR', 'STATE', 'ROA_HSU', 'AFFECTED_RATIO_lag1',
            'AFFECTED_RATIO_lag2', 'LOG_ASSETS', 'LEVERAGE']

reg_data = data[reg_vars].dropna()

print(f"✓ Observations after dropping NaN: {len(reg_data):,}")
print(f"✓ Companies in sample: {reg_data['PERMNO'].nunique()}")
print(f"✓ Mean ROA: {reg_data['ROA_HSU'].mean():.4f}")
print(f"✓ Mean AFFECTED_RATIO_lag1: {reg_data['AFFECTED_RATIO_lag1'].mean():.4f}")

# ============================================================================
# STEP 4: RUN CORRECTED REGRESSIONS
# ============================================================================

print("\n5. RUNNING CORRECTED REGRESSIONS...")
print("-"*80)

import statsmodels.formula.api as smf

# MODEL 1: Simple OLS with LAGGED exposure
print("\nMODEL 1: Simple OLS (with LAGGED exposure)")
print("-"*40)
model1 = smf.ols('ROA_HSU ~ AFFECTED_RATIO_lag1', data=reg_data).fit()
print(f"  Coefficient: {model1.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  Std Error:   {model1.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value:     {model1.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R-squared:   {model1.rsquared:.4f}")
print(f"  N:           {int(model1.nobs)}")

# MODEL 2: With controls
print("\nMODEL 2: With firm controls (LAGGED exposure)")
print("-"*40)
model2 = smf.ols('ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE',
                 data=reg_data).fit()
print(f"  AFFECTED_RATIO_lag1:")
print(f"    Coefficient: {model2.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"    Std Error:   {model2.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"    P-value:     {model2.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  LOG_ASSETS:")
print(f"    Coefficient: {model2.params['LOG_ASSETS']:.6f}")
print(f"    P-value:     {model2.pvalues['LOG_ASSETS']:.4f}")
print(f"  LEVERAGE:")
print(f"    Coefficient: {model2.params['LEVERAGE']:.6f}")
print(f"    P-value:     {model2.pvalues['LEVERAGE']:.4f}")
print(f"  R-squared:   {model2.rsquared:.4f}")
print(f"  N:           {int(model2.nobs)}")

# MODEL 3: With Year Fixed Effects
print("\nMODEL 3: With Year FE (LAGGED exposure)")
print("-"*40)
model3 = smf.ols('ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + C(YEAR)',
                 data=reg_data).fit()
print(f"  AFFECTED_RATIO_lag1:")
print(f"    Coefficient: {model3.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"    Std Error:   {model3.bse['AFFECTED_RATIO_lag1']:.6f}")
print(f"    P-value:     {model3.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R-squared:   {model3.rsquared:.4f}")
print(f"  N:           {int(model3.nobs)}")

# ============================================================================
# STEP 5: FIRM FIXED EFFECTS (CRITICAL FIX #3)
# ============================================================================

print("\n6. MODEL WITH FIRM FIXED EFFECTS...")
print("-"*80)

try:
    from linearmodels import PanelOLS

    # Set up panel data structure
    panel_data = reg_data.set_index(['PERMNO', 'YEAR'])

    # Model 4: Firm + Year Fixed Effects (Hsu et al. exact specification)
    model4 = PanelOLS.from_formula(
        'ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + TimeEffects',
        data=panel_data,
        entity_effects=True,  # Firm fixed effects (η_i)
        check_rank=False
    ).fit(cov_type='clustered', cluster_entity=True)

    print("MODEL 4: Two-way Fixed Effects (Hsu et al. specification)")
    print("-"*40)
    print(f"  AFFECTED_RATIO_lag1:")
    print(f"    Coefficient: {model4.params['AFFECTED_RATIO_lag1']:.6f}")
    print(f"    Std Error:   {model4.std_errors['AFFECTED_RATIO_lag1']:.6f}")
    print(f"    P-value:     {model4.pvalues['AFFECTED_RATIO_lag1']:.4f}")
    print(f"  R-squared (within): {model4.rsquared_within:.4f}")
    print(f"  N:           {int(model4.nobs)}")

    has_panel = True

except ImportError:
    print("⚠ linearmodels not installed. Install with: pip install linearmodels")
    print("  Falling back to entity dummies approach...")

    # Alternative: Include firm dummies manually (memory-intensive)
    model4 = smf.ols('ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + C(PERMNO) + C(YEAR)',
                     data=reg_data).fit()
    print("MODEL 4: Two-way FE (entity dummies)")
    print("-"*40)
    print(f"  AFFECTED_RATIO_lag1:")
    print(f"    Coefficient: {model4.params['AFFECTED_RATIO_lag1']:.6f}")
    print(f"    Std Error:   {model4.bse['AFFECTED_RATIO_lag1']:.6f}")
    print(f"    P-value:     {model4.pvalues['AFFECTED_RATIO_lag1']:.4f}")

    has_panel = False

# ============================================================================
# STEP 6: COMPARISON WITH ORIGINAL RESULTS
# ============================================================================

print("\n" + "="*80)
print("RESULTS COMPARISON")
print("="*80)

print("\n┌─────────────────────────────────────────────────────────────────────┐")
print("│                    CORRECTED vs ORIGINAL RESULTS                      │")
print("├─────────────────────────────────────────────────────────────────────┤")
print("│ Specification          │ Coefficient │ Std Error │ P-value │   N    │")
print("├─────────────────────────────────────────────────────────────────────┤")
print(f"│ ORIGINAL (contemp.)    │   +0.0042   │   0.0064  │  0.506  │  2080  │")
print("├─────────────────────────────────────────────────────────────────────┤")
print(f"│ CORRECTED Model 1      │ {model1.params['AFFECTED_RATIO_lag1']:+.6f} │ {model1.bse['AFFECTED_RATIO_lag1']:.6f} │ {model1.pvalues['AFFECTED_RATIO_lag1']:.4f} │ {int(model1.nobs):5d}  │")
print(f"│ CORRECTED Model 2      │ {model2.params['AFFECTED_RATIO_lag1']:+.6f} │ {model2.bse['AFFECTED_RATIO_lag1']:.6f} │ {model2.pvalues['AFFECTED_RATIO_lag1']:.4f} │ {int(model2.nobs):5d}  │")
print(f"│ CORRECTED Model 3      │ {model3.params['AFFECTED_RATIO_lag1']:+.6f} │ {model3.bse['AFFECTED_RATIO_lag1']:.6f} │ {model3.pvalues['AFFECTED_RATIO_lag1']:.4f} │ {int(model3.nobs):5d}  │")
print("├─────────────────────────────────────────────────────────────────────┤")
print(f"│ HSU ET AL. (2018)      │   -0.0120   │   0.0040  │ <0.010  │ 16709  │")
print("└─────────────────────────────────────────────────────────────────────┘")

# ============================================================================
# STEP 7: INTERPRETATION
# ============================================================================

print("\n" + "="*80)
print("INTERPRETATION")
print("="*80)

coef = model3.params['AFFECTED_RATIO_lag1']
pval = model3.pvalues['AFFECTED_RATIO_lag1']

print(f"""
Key Finding:
------------
After implementing the corrected methodology:
- Lagged AFFECTED_RATIO coefficient: {coef:.4f}
- P-value: {pval:.4f}
- Direction: {"NEGATIVE (matches Hsu et al.)" if coef < 0 else "POSITIVE (differs from Hsu et al.)"}
- Significance: {"SIGNIFICANT" if pval < 0.10 else "NOT SIGNIFICANT"} at 10% level

Interpretation:
---------------
{"The corrected results show a NEGATIVE relationship between lagged disaster exposure and ROA, consistent with Hsu et al. (2018)." if coef < 0 else "The corrected results still show a POSITIVE relationship, suggesting modern manufacturing firms (2016-2023) may be more resilient than the Hsu et al. sample (1987-2014)."}

Remaining Differences from Hsu et al.:
--------------------------------------
1. Different time period (2016-2023 vs 1987-2014)
2. Smaller sample size ({int(model3.nobs)} vs 16,709)
3. May need OIBDP instead of Net Income for exact replication
4. Consider filtering to major disasters only

NOTE: Results shown are based on SAMPLE DATA for demonstration.
      Run with ACTUAL data for true results.
""")

# ============================================================================
# STEP 8: SAVE RESULTS
# ============================================================================

print("\n" + "="*80)
print("SAVING RESULTS...")
print("="*80)

# Create results summary DataFrame
results_summary = pd.DataFrame({
    'Model': ['Original (Contemporaneous)', 'Corrected Model 1', 'Corrected Model 2',
              'Corrected Model 3', 'Hsu et al. (2018)'],
    'Specification': ['ROA ~ AFFECTED_RATIO', 'ROA_HSU ~ AFFECTED_RATIO_lag1',
                      '+ LOG_ASSETS + LEVERAGE', '+ Year FE', 'Firm FE + Year FE'],
    'Coefficient': [0.0042, model1.params['AFFECTED_RATIO_lag1'],
                   model2.params['AFFECTED_RATIO_lag1'], model3.params['AFFECTED_RATIO_lag1'],
                   -0.0120],
    'Std_Error': [0.0064, model1.bse['AFFECTED_RATIO_lag1'],
                 model2.bse['AFFECTED_RATIO_lag1'], model3.bse['AFFECTED_RATIO_lag1'],
                 0.0040],
    'P_value': [0.506, model1.pvalues['AFFECTED_RATIO_lag1'],
               model2.pvalues['AFFECTED_RATIO_lag1'], model3.pvalues['AFFECTED_RATIO_lag1'],
               0.001],
    'N': [2080, int(model1.nobs), int(model2.nobs), int(model3.nobs), 16709],
    'Lagged': ['No', 'Yes', 'Yes', 'Yes', 'Yes'],
    'ROA_Definition': ['NI/AT', 'OIBDP/lag(AT)', 'OIBDP/lag(AT)', 'OIBDP/lag(AT)', 'OIBDP/lag(AT)']
})

# Save to CSV
results_file = 'CORRECTED_RESULTS.csv'
results_summary.to_csv(results_file, index=False)
print(f"✓ Saved: {results_file}")

# Save corrected data
corrected_data_file = 'CORRECTED_DATASET.csv'
data.to_csv(corrected_data_file, index=False)
print(f"✓ Saved: {corrected_data_file}")

print("\n" + "="*80)
print("✅ CORRECTED ANALYSIS COMPLETE")
print("="*80)
print("""
Files Generated:
----------------
1. CORRECTED_RESULTS.csv - Comparison of original vs corrected results
2. CORRECTED_DATASET.csv - Dataset with lagged variables

Next Steps:
-----------
1. Replace sample data with actual data from Notebooks 1-5
2. Load OIBDP from Compustat for exact ROA calculation
3. Add firm fixed effects using linearmodels package
4. Cluster standard errors at state level
5. Consider filtering to major disasters only
""")
