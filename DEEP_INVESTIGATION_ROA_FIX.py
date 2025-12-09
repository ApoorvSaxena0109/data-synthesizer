#!/usr/bin/env python3
"""
DEEP INVESTIGATION: ROA Calculation Fix
========================================

CRITICAL FINDING FROM AUDIT:
The POSITIVE coefficient (+0.007) persists even after lagging because
the ROA calculation is fundamentally wrong.

CURRENT ROA:    Net Income / Total Assets = 0.055 mean
HSU ET AL. ROA: OIBDP / Lagged Total Assets = 0.160 mean

This 3x difference in mean ROA indicates a completely different measure!

This script:
1. Investigates what financial variables are actually available
2. Creates CORRECT ROA using Hsu et al. definition
3. Tests if correlation sign changes with corrected ROA
4. Runs regressions with firm fixed effects

Author: Audit Correction
Date: December 2025
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("DEEP INVESTIGATION: ROA CALCULATION FIX")
print("="*80)

# ============================================================================
# SECTION 1: THE PROBLEM
# ============================================================================

print("""
================================================================================
THE PROBLEM: WHY LAGGING ALONE DIDN'T FIX THE POSITIVE COEFFICIENT
================================================================================

CURRENT SITUATION:
- Coefficient: +0.0070 (POSITIVE!)
- P-value: 0.216 (NOT significant)
- Correlation ROA ↔ AFFECTED_RATIO_lag1: +0.0177 (POSITIVE!)

HSU ET AL. (2018):
- Coefficient: -0.012 (NEGATIVE!)
- P-value: <0.01 (HIGHLY significant)

LIKELY ROOT CAUSE: WRONG ROA DEFINITION

┌─────────────────────────────────────────────────────────────────────────────┐
│                    ROA CALCULATION COMPARISON                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  CURRENT IMPLEMENTATION:                                                     │
│     ROA = Net Income(t) / Total Assets(t)                                    │
│     Mean ROA = 0.055 (5.5%)                                                  │
│                                                                              │
│  HSU ET AL. (2018) DEFINITION:                                               │
│     ROA = OIBDP(t) / Total Assets(t-1)                                       │
│     Mean ROA = 0.160 (16.0%)                                                 │
│                                                                              │
│  DIFFERENCE: Their ROA is 3x HIGHER because:                                 │
│     1. OIBDP > Net Income (no depreciation, interest, taxes deducted)        │
│     2. Lagged assets in denominator (assets typically grow)                  │
└─────────────────────────────────────────────────────────────────────────────┘

WHAT IS OIBDP?
--------------
OIBDP = Operating Income Before Depreciation (Compustat variable 'oibdp')

Income Statement Progression:
    Revenue
    - Cost of Goods Sold
    - Selling, General & Administrative
    ─────────────────────────────
    = OIBDP (Operating Income Before Depreciation)  ← HSU ET AL. USE THIS

    - Depreciation & Amortization
    ─────────────────────────────
    = Operating Income (EBIT)

    - Interest Expense
    ─────────────────────────────
    = Earnings Before Tax

    - Income Tax
    ─────────────────────────────
    = Net Income  ← WHAT YOU CURRENTLY USE

OIBDP is typically 2-4x larger than Net Income!
""")

# ============================================================================
# SECTION 2: CHECK WHAT VARIABLES ARE AVAILABLE
# ============================================================================

print("\n" + "="*80)
print("SECTION 2: CHECKING AVAILABLE FINANCIAL VARIABLES")
print("="*80)

# List of Compustat variables that could approximate OIBDP
compustat_vars = {
    'oibdp': 'Operating Income Before Depreciation (EXACT - what Hsu et al. use)',
    'ebitda': 'Earnings Before Interest, Taxes, Depreciation & Amortization',
    'oiadp': 'Operating Income After Depreciation',
    'dp': 'Depreciation and Amortization',
    'ni': 'Net Income',
    'ib': 'Income Before Extraordinary Items',
    'revt': 'Total Revenue',
    'cogs': 'Cost of Goods Sold',
    'xsga': 'Selling, General & Administrative Expense',
    'xint': 'Interest and Related Expense',
    'txt': 'Income Taxes',
    'at': 'Total Assets'
}

print("\nCompustat variables that could help calculate OIBDP:")
print("-"*80)
for var, desc in compustat_vars.items():
    print(f"  {var:8s} : {desc}")

print("""
APPROXIMATION OPTIONS:

Option A (BEST): Use OIBDP directly if available
    ROA = oibdp / lag(at)

Option B: Use EBITDA as proxy
    ROA = ebitda / lag(at)
    (Note: EBITDA ≈ OIBDP for most firms)

Option C: Calculate from components
    OIBDP = revt - cogs - xsga
    ROA = OIBDP / lag(at)

Option D: Back-calculate from Net Income
    OIBDP = ni + dp + xint + txt
    ROA = OIBDP / lag(at)
    (Requires depreciation, interest, and tax data)

Option E (MINIMUM FIX): Just use lagged assets
    ROA = ni / lag(at)
    (Still wrong numerator, but fixes denominator)
""")

# ============================================================================
# SECTION 3: CODE TO CHECK YOUR ACTUAL DATA
# ============================================================================

print("\n" + "="*80)
print("SECTION 3: CODE TO CHECK YOUR DATA")
print("="*80)

check_code = '''
# ============================================================================
# RUN THIS CODE IN YOUR COLAB NOTEBOOK TO CHECK AVAILABLE VARIABLES
# ============================================================================

from pathlib import Path
import pandas as pd

BASE_PATH = Path('/content/drive/MyDrive/Paper1_Dataset')
PROCESSED_PATH = BASE_PATH / 'processed'

# Load your current financial data
financial_data = pd.read_parquet(PROCESSED_PATH / 'company_year_panel_with_affected_ratio.parquet')

print("="*80)
print("COLUMNS IN YOUR FINANCIAL DATA:")
print("="*80)
print(financial_data.columns.tolist())

print("\\n" + "="*80)
print("CHECKING FOR KEY VARIABLES:")
print("="*80)

key_vars = ['OIBDP', 'oibdp', 'EBITDA', 'ebitda', 'OPERATING_INCOME',
            'DEPRECIATION', 'dp', 'DP', 'INTEREST_EXPENSE', 'xint',
            'INCOME_TAX', 'txt', 'NET_INCOME', 'ni', 'TOTAL_ASSETS', 'at']

for var in key_vars:
    if var in financial_data.columns:
        non_null = financial_data[var].notna().sum()
        print(f"  ✓ {var}: {non_null:,} non-null values")
    elif var.upper() in financial_data.columns:
        non_null = financial_data[var.upper()].notna().sum()
        print(f"  ✓ {var.upper()}: {non_null:,} non-null values")
    elif var.lower() in financial_data.columns:
        non_null = financial_data[var.lower()].notna().sum()
        print(f"  ✓ {var.lower()}: {non_null:,} non-null values")

# Also check the original Compustat files
print("\\n" + "="*80)
print("CHECKING ORIGINAL COMPUSTAT FILES:")
print("="*80)

# Look for raw Compustat files
import glob
compustat_files = list(BASE_PATH.glob('*compustat*')) + list(BASE_PATH.glob('*Compustat*'))
compustat_files += list(BASE_PATH.glob('raw/*compustat*')) + list(BASE_PATH.glob('raw/*Compustat*'))

print(f"Found {len(compustat_files)} potential Compustat files:")
for f in compustat_files:
    print(f"  - {f.name}")
'''

print(check_code)

# ============================================================================
# SECTION 4: CODE TO CREATE CORRECTED ROA
# ============================================================================

print("\n" + "="*80)
print("SECTION 4: CODE TO CREATE CORRECTED ROA")
print("="*80)

fix_code = '''
# ============================================================================
# CODE TO CREATE CORRECTED ROA (ADD TO YOUR NOTEBOOK)
# ============================================================================

# Step 1: Sort data by company and year (CRITICAL for lagging)
analysis_data = analysis_data.sort_values(['PERMNO', 'YEAR']).reset_index(drop=True)

# Step 2: Create lagged total assets (for denominator)
analysis_data['AT_lag1'] = analysis_data.groupby('PERMNO')['TOTAL_ASSETS'].shift(1)

# Step 3: Create corrected ROA (choose based on what variables you have)

# ===== OPTION A: If you have OIBDP =====
if 'OIBDP' in analysis_data.columns:
    analysis_data['ROA_HSU'] = analysis_data['OIBDP'] / analysis_data['AT_lag1']
    print("✓ Using OIBDP / lagged Assets (Hsu et al. exact definition)")

# ===== OPTION B: If you have EBITDA =====
elif 'EBITDA' in analysis_data.columns:
    analysis_data['ROA_HSU'] = analysis_data['EBITDA'] / analysis_data['AT_lag1']
    print("✓ Using EBITDA / lagged Assets (close approximation)")

# ===== OPTION C: Back-calculate OIBDP from Net Income + Depreciation =====
elif 'DEPRECIATION' in analysis_data.columns:
    # OIBDP ≈ Net Income + Depreciation + Interest + Taxes
    # Minimum: OIBDP ≈ Net Income + Depreciation
    analysis_data['OIBDP_approx'] = analysis_data['NET_INCOME'] + analysis_data['DEPRECIATION']
    analysis_data['ROA_HSU'] = analysis_data['OIBDP_approx'] / analysis_data['AT_lag1']
    print("✓ Using (Net Income + Depreciation) / lagged Assets (approximation)")

# ===== OPTION D: Just fix denominator (minimum fix) =====
else:
    analysis_data['ROA_HSU'] = analysis_data['NET_INCOME'] / analysis_data['AT_lag1']
    print("⚠ Using Net Income / lagged Assets (minimum fix - still wrong numerator!)")
    print("  You SHOULD get OIBDP from Compustat for accurate replication")

# Step 4: Compare original vs corrected ROA
print("\\n" + "="*80)
print("ROA COMPARISON: Original vs Corrected")
print("="*80)
print(f"Original ROA (NI/AT):")
print(f"  Mean:   {analysis_data['ROA'].mean():.4f}")
print(f"  Median: {analysis_data['ROA'].median():.4f}")
print(f"  Std:    {analysis_data['ROA'].std():.4f}")

print(f"\\nCorrected ROA (OIBDP/lag_AT or approximation):")
print(f"  Mean:   {analysis_data['ROA_HSU'].mean():.4f}")
print(f"  Median: {analysis_data['ROA_HSU'].median():.4f}")
print(f"  Std:    {analysis_data['ROA_HSU'].std():.4f}")

print(f"\\nHsu et al. (2018) benchmark:")
print(f"  Mean:   0.1600")

# Step 5: Check if correlation sign changes!
print("\\n" + "="*80)
print("CRITICAL TEST: CORRELATION SIGN")
print("="*80)

corr_original = analysis_data[['ROA', 'AFFECTED_RATIO_lag1']].corr().iloc[0,1]
corr_corrected = analysis_data[['ROA_HSU', 'AFFECTED_RATIO_lag1']].dropna().corr().iloc[0,1]

print(f"Original ROA ↔ AFFECTED_RATIO_lag1:  {corr_original:+.4f}")
print(f"Corrected ROA ↔ AFFECTED_RATIO_lag1: {corr_corrected:+.4f}")

if corr_original > 0 and corr_corrected < 0:
    print("\\n🎉 SUCCESS! Correlation sign FLIPPED from positive to negative!")
    print("   This confirms ROA definition was the problem.")
elif corr_corrected < corr_original:
    print("\\n⚠ Correlation became more negative (or less positive)")
    print("   ROA definition was part of the problem, but maybe not all of it.")
else:
    print("\\n❌ Correlation did not improve significantly.")
    print("   Need to investigate other factors (firm FE, data quality, etc.)")
'''

print(fix_code)

# ============================================================================
# SECTION 5: CODE FOR FIRM FIXED EFFECTS
# ============================================================================

print("\n" + "="*80)
print("SECTION 5: FIRM FIXED EFFECTS REGRESSION")
print("="*80)

fe_code = '''
# ============================================================================
# FIRM FIXED EFFECTS REGRESSION (Hsu et al. exact specification)
# ============================================================================

# Install linearmodels if not already installed
# !pip install linearmodels

from linearmodels import PanelOLS
import statsmodels.formula.api as smf

# Prepare data for panel regression
# Must have valid ROA_HSU and AFFECTED_RATIO_lag1
reg_data = analysis_data[['PERMNO', 'YEAR', 'ROA_HSU', 'AFFECTED_RATIO_lag1',
                          'LOG_ASSETS', 'LEVERAGE']].dropna()

print(f"Panel regression sample: {len(reg_data):,} observations")
print(f"Unique firms: {reg_data['PERMNO'].nunique()}")

# Set up panel index
panel_data = reg_data.set_index(['PERMNO', 'YEAR'])

# ============================================================================
# MODEL 4: TWO-WAY FIXED EFFECTS (Hsu et al. specification)
# ============================================================================
print("\\n" + "="*80)
print("MODEL 4: TWO-WAY FIXED EFFECTS (Hsu et al. exact specification)")
print("ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + Firm_FE + Year_FE")
print("="*80)

try:
    model_fe = PanelOLS.from_formula(
        'ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + TimeEffects',
        data=panel_data,
        entity_effects=True,    # Firm fixed effects (η_i)
        time_effects=True,      # Year fixed effects (μ_t)
        check_rank=False
    ).fit(cov_type='clustered', cluster_entity=True)

    print(model_fe.summary)

    print("\\n" + "-"*80)
    print("KEY RESULT:")
    print("-"*80)
    coef = model_fe.params['AFFECTED_RATIO_lag1']
    se = model_fe.std_errors['AFFECTED_RATIO_lag1']
    pval = model_fe.pvalues['AFFECTED_RATIO_lag1']

    print(f"AFFECTED_RATIO_lag1 coefficient: {coef:.6f}")
    print(f"Standard error (clustered):       {se:.6f}")
    print(f"P-value:                          {pval:.4f}")

    if coef < 0:
        print(f"\\n✓ NEGATIVE coefficient - matches Hsu et al. direction!")
    else:
        print(f"\\n⚠ POSITIVE coefficient - still differs from Hsu et al.")

except ImportError:
    print("linearmodels not installed. Using statsmodels with entity dummies instead...")

    # Alternative: OLS with firm dummies (memory-intensive for large N)
    model_fe = smf.ols(
        'ROA_HSU ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + C(PERMNO) + C(YEAR)',
        data=reg_data
    ).fit()

    print(f"AFFECTED_RATIO_lag1 coefficient: {model_fe.params['AFFECTED_RATIO_lag1']:.6f}")
    print(f"P-value: {model_fe.pvalues['AFFECTED_RATIO_lag1']:.4f}")
'''

print(fe_code)

# ============================================================================
# SECTION 6: COMPREHENSIVE COMPARISON TABLE
# ============================================================================

print("\n" + "="*80)
print("SECTION 6: COMPARISON TABLE CODE")
print("="*80)

comparison_code = '''
# ============================================================================
# CREATE COMPREHENSIVE COMPARISON TABLE
# ============================================================================

print("\\n" + "="*80)
print("COMPREHENSIVE RESULTS COMPARISON")
print("="*80)

# Collect all results
results = []

# Original wrong specification
results.append({
    'Specification': 'Original (NI/AT, contemporaneous)',
    'ROA Definition': 'Net Income / Assets(t)',
    'Lagging': 'No',
    'Firm FE': 'No',
    'Coefficient': '+0.0042',  # From your Notebook 5
    'P-value': '0.506',
    'Note': 'WRONG - matches your current results'
})

# Your corrected with lagging (but wrong ROA)
results.append({
    'Specification': 'With Lagging (NI/AT)',
    'ROA Definition': 'Net Income / Assets(t)',
    'Lagging': 'Yes (t-1)',
    'Firm FE': 'No',
    'Coefficient': '+0.0070',  # From your lagged analysis
    'P-value': '0.216',
    'Note': 'Still wrong ROA definition'
})

# After this fix (minimum - lagged assets)
# Fill in after running the corrected code
results.append({
    'Specification': 'Corrected ROA Denominator',
    'ROA Definition': 'Net Income / Assets(t-1)',
    'Lagging': 'Yes (t-1)',
    'Firm FE': 'No',
    'Coefficient': '???',  # Fill in
    'P-value': '???',
    'Note': 'Run code to get this'
})

# Full Hsu et al. spec
results.append({
    'Specification': 'Full Hsu et al. (2018)',
    'ROA Definition': 'OIBDP / Assets(t-1)',
    'Lagging': 'Yes (t-1)',
    'Firm FE': 'Yes',
    'Coefficient': '???',  # Fill in
    'P-value': '???',
    'Note': 'Run code to get this'
})

# Hsu et al. benchmark
results.append({
    'Specification': 'Hsu et al. (2018) Paper',
    'ROA Definition': 'OIBDP / Assets(t-1)',
    'Lagging': 'Yes (t-1)',
    'Firm FE': 'Yes',
    'Coefficient': '-0.0120',
    'P-value': '<0.01',
    'Note': 'Target to replicate'
})

comparison_df = pd.DataFrame(results)
print(comparison_df.to_string(index=False))

# Save
comparison_df.to_csv('RESULTS_COMPARISON_TABLE.csv', index=False)
print("\\n✓ Saved: RESULTS_COMPARISON_TABLE.csv")
'''

print(comparison_code)

# ============================================================================
# SECTION 7: STEP-BY-STEP ACTION PLAN
# ============================================================================

print("\n" + "="*80)
print("SECTION 7: STEP-BY-STEP ACTION PLAN")
print("="*80)

print("""
================================================================================
STEP-BY-STEP ACTION PLAN TO FIX THE POSITIVE COEFFICIENT
================================================================================

STEP 1: CHECK YOUR COMPUSTAT DATA FOR OIBDP
------------------------------------------
Run the code in Section 3 in your Colab notebook to check what variables
are available. Look for:
- OIBDP or oibdp (best)
- EBITDA or ebitda (good alternative)
- DEPRECIATION or dp (for back-calculation)

STEP 2: LOAD OIBDP FROM ORIGINAL COMPUSTAT
------------------------------------------
If OIBDP is not in your current dataset but exists in the original
Compustat files, you need to:

a) Find the raw Compustat file(s)
b) Extract the 'oibdp' variable
c) Merge with your existing data

Code:
```python
# Load raw Compustat
compustat_raw = pd.read_csv(BASE_PATH / 'raw' / 'compustat_annual.csv')

# Check columns
print(compustat_raw.columns.tolist())

# Extract OIBDP
oibdp_data = compustat_raw[['gvkey', 'fyear', 'oibdp', 'at']].copy()
oibdp_data.columns = ['GVKEY', 'YEAR', 'OIBDP', 'AT']

# Merge with your data (need GVKEY-PERMNO link)
```

STEP 3: CREATE LAGGED ASSETS (MINIMUM FIX)
------------------------------------------
Even if you can't get OIBDP, you MUST fix the denominator:

```python
analysis_data = analysis_data.sort_values(['PERMNO', 'YEAR'])
analysis_data['AT_lag1'] = analysis_data.groupby('PERMNO')['TOTAL_ASSETS'].shift(1)
analysis_data['ROA_corrected'] = analysis_data['NET_INCOME'] / analysis_data['AT_lag1']
```

STEP 4: CHECK CORRELATION SIGN
------------------------------
After creating corrected ROA, check if correlation becomes negative:

```python
corr = analysis_data[['ROA_corrected', 'AFFECTED_RATIO_lag1']].dropna().corr()
print(f"Correlation: {corr.iloc[0,1]:.4f}")
```

If correlation becomes NEGATIVE → ROA definition was the main problem!
If correlation stays POSITIVE → May need firm fixed effects or other fixes

STEP 5: RUN FIRM FIXED EFFECTS REGRESSION
-----------------------------------------
Install linearmodels and run panel regression:

```python
!pip install linearmodels
from linearmodels import PanelOLS

panel_data = reg_data.set_index(['PERMNO', 'YEAR'])
model = PanelOLS.from_formula(
    'ROA_corrected ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + TimeEffects',
    data=panel_data,
    entity_effects=True,
    time_effects=True
).fit(cov_type='clustered', cluster_entity=True)
print(model.summary)
```

STEP 6: DOCUMENT FINDINGS
-------------------------
After implementing fixes:
1. Update AUDIT_REPORT.md with new findings
2. Create comparison table showing progression
3. Explain any remaining differences from Hsu et al.

================================================================================
EXPECTED OUTCOMES
================================================================================

AFTER LAGGED ASSETS FIX:
- ROA mean should INCREASE (smaller denominator)
- Correlation may shift toward negative

AFTER OIBDP FIX:
- ROA mean should be ~0.10-0.16 (closer to Hsu et al.'s 0.16)
- Correlation should become NEGATIVE

AFTER FIRM FIXED EFFECTS:
- Coefficient should be more NEGATIVE
- Standard errors may increase (fewer degrees of freedom)
- Significance may improve if true effect is negative

IF COEFFICIENT REMAINS POSITIVE AFTER ALL FIXES:
- This is a LEGITIMATE FINDING
- Modern manufacturing firms (2016-2023) may be more resilient
- Document as difference from Hsu et al. due to time period
- Possible reasons: better insurance, supply chain diversification,
  improved disaster preparedness

================================================================================
""")

# ============================================================================
# SECTION 8: COMPLETE CORRECTED NOTEBOOK CODE
# ============================================================================

print("\n" + "="*80)
print("SECTION 8: COMPLETE CORRECTED NOTEBOOK CODE")
print("="*80)
print("(Copy this entire code block to a new notebook cell)")
print("="*80)

complete_code = '''
# ============================================================================
# COMPLETE CORRECTED ANALYSIS CODE
# Copy this to a new cell in your Colab notebook after loading data
# ============================================================================

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

print("="*80)
print("CORRECTED ANALYSIS: HSU ET AL. (2018) REPLICATION")
print("="*80)

# ============================================================================
# STEP 1: CREATE LAGGED VARIABLES
# ============================================================================
print("\\nStep 1: Creating lagged variables...")

analysis_data = analysis_data.sort_values(['PERMNO', 'YEAR']).reset_index(drop=True)

# Lagged disaster exposure (t-1)
analysis_data['AFFECTED_RATIO_lag1'] = analysis_data.groupby('PERMNO')['AFFECTED_RATIO'].shift(1)

# Lagged total assets for ROA denominator (t-1)
analysis_data['AT_lag1'] = analysis_data.groupby('PERMNO')['TOTAL_ASSETS'].shift(1)

print(f"  ✓ Created AFFECTED_RATIO_lag1")
print(f"  ✓ Created AT_lag1 (lagged total assets)")

# ============================================================================
# STEP 2: CREATE CORRECTED ROA
# ============================================================================
print("\\nStep 2: Creating corrected ROA...")

# Check what's available for numerator
if 'OIBDP' in analysis_data.columns:
    analysis_data['ROA_corrected'] = analysis_data['OIBDP'] / analysis_data['AT_lag1']
    roa_type = "OIBDP / lag(AT) - Hsu et al. exact"
elif 'EBITDA' in analysis_data.columns:
    analysis_data['ROA_corrected'] = analysis_data['EBITDA'] / analysis_data['AT_lag1']
    roa_type = "EBITDA / lag(AT) - close proxy"
elif 'DEPRECIATION' in analysis_data.columns:
    analysis_data['OIBDP_approx'] = analysis_data['NET_INCOME'] + analysis_data['DEPRECIATION']
    analysis_data['ROA_corrected'] = analysis_data['OIBDP_approx'] / analysis_data['AT_lag1']
    roa_type = "(NI + Depreciation) / lag(AT) - approximation"
else:
    # Minimum fix: just use lagged assets
    analysis_data['ROA_corrected'] = analysis_data['NET_INCOME'] / analysis_data['AT_lag1']
    roa_type = "NI / lag(AT) - minimum fix"
    print("  ⚠ WARNING: OIBDP not available. Using Net Income (not ideal)")

print(f"  ✓ ROA formula: {roa_type}")

# ============================================================================
# STEP 3: COMPARE ROA DISTRIBUTIONS
# ============================================================================
print("\\n" + "="*80)
print("ROA COMPARISON")
print("="*80)

# Original ROA
print(f"\\nOriginal ROA (NI / AT):")
print(f"  Mean:   {analysis_data['ROA'].mean():.4f}")
print(f"  Median: {analysis_data['ROA'].median():.4f}")
print(f"  Std:    {analysis_data['ROA'].std():.4f}")

# Corrected ROA
valid_roa = analysis_data['ROA_corrected'].dropna()
print(f"\\nCorrected ROA ({roa_type}):")
print(f"  Mean:   {valid_roa.mean():.4f}")
print(f"  Median: {valid_roa.median():.4f}")
print(f"  Std:    {valid_roa.std():.4f}")

print(f"\\nHsu et al. (2018) benchmark:")
print(f"  Mean:   0.1600")
print(f"  Your mean is {valid_roa.mean()/0.16*100:.0f}% of theirs")

# ============================================================================
# STEP 4: CRITICAL TEST - CORRELATION SIGN
# ============================================================================
print("\\n" + "="*80)
print("CRITICAL TEST: CORRELATION SIGN")
print("="*80)

# Prepare data with non-missing values
test_data = analysis_data[['ROA', 'ROA_corrected', 'AFFECTED_RATIO_lag1']].dropna()

corr_original = test_data['ROA'].corr(test_data['AFFECTED_RATIO_lag1'])
corr_corrected = test_data['ROA_corrected'].corr(test_data['AFFECTED_RATIO_lag1'])

print(f"\\nOriginal ROA ↔ AFFECTED_RATIO_lag1:  {corr_original:+.4f}")
print(f"Corrected ROA ↔ AFFECTED_RATIO_lag1: {corr_corrected:+.4f}")

if corr_original > 0 and corr_corrected < 0:
    print("\\n" + "🎉"*20)
    print("SUCCESS! Correlation sign FLIPPED from positive to negative!")
    print("This confirms ROA definition was the main problem.")
    print("🎉"*20)
elif corr_corrected < corr_original:
    print("\\n⚠ Correlation became more negative (or less positive)")
    print("   ROA definition was part of the problem.")
else:
    print("\\n❌ Correlation did not improve. May need firm fixed effects.")

# ============================================================================
# STEP 5: RUN REGRESSIONS WITH CORRECTED ROA
# ============================================================================
print("\\n" + "="*80)
print("REGRESSIONS WITH CORRECTED ROA")
print("="*80)

# Prepare regression data
reg_vars = ['ROA_corrected', 'AFFECTED_RATIO_lag1', 'LOG_ASSETS', 'LEVERAGE', 'YEAR', 'PERMNO']
reg_data = analysis_data[reg_vars].dropna()

print(f"\\nRegression sample: {len(reg_data):,} observations")
print(f"Companies: {reg_data['PERMNO'].nunique()}")

# Model 1: Simple OLS
print("\\n" + "-"*40)
print("Model 1: Simple OLS")
model1 = smf.ols('ROA_corrected ~ AFFECTED_RATIO_lag1', data=reg_data).fit()
print(f"  Coefficient: {model1.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value:     {model1.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R-squared:   {model1.rsquared:.4f}")

# Model 2: With controls
print("\\n" + "-"*40)
print("Model 2: With Controls")
model2 = smf.ols('ROA_corrected ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE',
                 data=reg_data).fit()
print(f"  Coefficient: {model2.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value:     {model2.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R-squared:   {model2.rsquared:.4f}")

# Model 3: With Year FE
print("\\n" + "-"*40)
print("Model 3: With Year Fixed Effects")
model3 = smf.ols('ROA_corrected ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + C(YEAR)',
                 data=reg_data).fit()
print(f"  Coefficient: {model3.params['AFFECTED_RATIO_lag1']:.6f}")
print(f"  P-value:     {model3.pvalues['AFFECTED_RATIO_lag1']:.4f}")
print(f"  R-squared:   {model3.rsquared:.4f}")

# ============================================================================
# STEP 6: FIRM FIXED EFFECTS (if linearmodels available)
# ============================================================================
print("\\n" + "-"*40)
print("Model 4: Two-way Fixed Effects (Hsu et al. specification)")
try:
    from linearmodels import PanelOLS

    panel_data = reg_data.set_index(['PERMNO', 'YEAR'])
    model4 = PanelOLS.from_formula(
        'ROA_corrected ~ AFFECTED_RATIO_lag1 + LOG_ASSETS + LEVERAGE + TimeEffects',
        data=panel_data,
        entity_effects=True,
        time_effects=True,
        check_rank=False
    ).fit(cov_type='clustered', cluster_entity=True)

    print(f"  Coefficient: {model4.params['AFFECTED_RATIO_lag1']:.6f}")
    print(f"  P-value:     {model4.pvalues['AFFECTED_RATIO_lag1']:.4f}")
    print(f"  R-squared:   {model4.rsquared_within:.4f} (within)")
    has_fe = True
except ImportError:
    print("  ⚠ linearmodels not installed. Skipping firm fixed effects.")
    print("  Install with: !pip install linearmodels")
    has_fe = False

# ============================================================================
# STEP 7: SUMMARY COMPARISON
# ============================================================================
print("\\n" + "="*80)
print("RESULTS COMPARISON")
print("="*80)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RESULTS COMPARISON                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Specification                │ Coefficient │ P-value │ ROA Definition       │
├─────────────────────────────────────────────────────────────────────────────┤""")

# Original (from your data)
print(f"│ Original (your Notebook 5)  │   +0.0042   │  0.506  │ NI / AT(t)           │")
print(f"│ With Lagging Only           │   +0.0070   │  0.216  │ NI / AT(t)           │")
print(f"│ Corrected Model 1           │ {model1.params['AFFECTED_RATIO_lag1']:+.6f} │ {model1.pvalues['AFFECTED_RATIO_lag1']:.4f}  │ {roa_type[:20]}│")
print(f"│ Corrected Model 2           │ {model2.params['AFFECTED_RATIO_lag1']:+.6f} │ {model2.pvalues['AFFECTED_RATIO_lag1']:.4f}  │ {roa_type[:20]}│")
print(f"│ Corrected Model 3 (Year FE) │ {model3.params['AFFECTED_RATIO_lag1']:+.6f} │ {model3.pvalues['AFFECTED_RATIO_lag1']:.4f}  │ {roa_type[:20]}│")
if has_fe:
    print(f"│ Corrected Model 4 (Firm FE) │ {model4.params['AFFECTED_RATIO_lag1']:+.6f} │ {model4.pvalues['AFFECTED_RATIO_lag1']:.4f}  │ {roa_type[:20]}│")
print(f"│ Hsu et al. (2018)           │   -0.0120   │ <0.010  │ OIBDP / lag(AT)      │")
print("└─────────────────────────────────────────────────────────────────────────────┘")

# Save results
results_df = pd.DataFrame({
    'Model': ['Original', 'With Lagging', 'Corrected M1', 'Corrected M2', 'Corrected M3'],
    'Coefficient': [0.0042, 0.0070,
                   model1.params['AFFECTED_RATIO_lag1'],
                   model2.params['AFFECTED_RATIO_lag1'],
                   model3.params['AFFECTED_RATIO_lag1']],
    'P_value': [0.506, 0.216,
               model1.pvalues['AFFECTED_RATIO_lag1'],
               model2.pvalues['AFFECTED_RATIO_lag1'],
               model3.pvalues['AFFECTED_RATIO_lag1']],
    'ROA_Definition': ['NI/AT(t)', 'NI/AT(t)', roa_type, roa_type, roa_type],
    'Lagging': ['No', 'Yes', 'Yes', 'Yes', 'Yes'],
    'Year_FE': ['Yes', 'Yes', 'No', 'No', 'Yes'],
    'Firm_FE': ['No', 'No', 'No', 'No', 'No']
})

if has_fe:
    results_df = pd.concat([results_df, pd.DataFrame({
        'Model': ['Corrected M4'],
        'Coefficient': [model4.params['AFFECTED_RATIO_lag1']],
        'P_value': [model4.pvalues['AFFECTED_RATIO_lag1']],
        'ROA_Definition': [roa_type],
        'Lagging': ['Yes'],
        'Year_FE': ['Yes'],
        'Firm_FE': ['Yes']
    })], ignore_index=True)

results_df.to_csv('CORRECTED_RESULTS_COMPARISON.csv', index=False)
print("\\n✓ Results saved to: CORRECTED_RESULTS_COMPARISON.csv")

print("\\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
'''

print(complete_code)

print("\n" + "="*80)
print("SCRIPT COMPLETE")
print("="*80)
print("""
This script provides:
1. Diagnosis of the ROA calculation problem
2. Code to check your available variables
3. Code to create corrected ROA
4. Code for firm fixed effects regressions
5. Comprehensive comparison table

NEXT STEPS:
1. Copy the code from Sections 3-8 into your Colab notebook
2. Run the variable check first
3. Create corrected ROA based on available variables
4. Run regressions and check if coefficient becomes negative

If you have any questions, refer back to the AUDIT_REPORT.md for full context.
""")
