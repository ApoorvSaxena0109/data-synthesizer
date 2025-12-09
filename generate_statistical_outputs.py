#!/usr/bin/env python3
"""
Statistical Analysis Output Generator - CONSOLIDATED (2 Files)
===============================================================
This script generates consolidated statistical analysis outputs for Professor Yang:
1. COMPLETE_DATA.xlsx - All data-related information (5 sheets)
2. COMPLETE_RESULTS.xlsx - All statistical results (10 sheets)

Replaces the previous multiple-file approach with a streamlined 2-file system
for easier review and debugging.

Output Files:
-------------
COMPLETE_DATA.xlsx contains:
  - Dataset Description
  - Descriptive Statistics
  - Data Dictionary
  - Exposure Distribution
  - Yearly Statistics

COMPLETE_RESULTS.xlsx contains:
  - Model Specification
  - Correlation Matrix Notes
  - Model 1, 2, 3 Results (coefficients and statistics)
  - Regression Summary
  - Publication-Ready Table

Author: Apoorv Saxena
Date: December 2025
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import sys
from datetime import datetime

print("="*80)
print("STATISTICAL ANALYSIS OUTPUT GENERATOR - CONSOLIDATED (2 FILES)")
print("="*80)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Output: COMPLETE_DATA.xlsx + COMPLETE_RESULTS.xlsx")
print("="*80)

# ============================================================================
# 1. EXTRACT DATA FROM NOTEBOOK OUTPUTS
# ============================================================================

print("\n1. Extracting analysis data from notebooks...")

# Read the regression notebook to extract outputs
notebook_path = Path('05_CLEAN_affected_ratio_baseline_regression.ipynb')

if not notebook_path.exists():
    print(f"ERROR: Notebook not found at {notebook_path}")
    sys.exit(1)

with open(notebook_path) as f:
    nb = json.load(f)

print(f"   ✓ Loaded notebook with {len(nb['cells'])} cells")

# ============================================================================
# 2. RECREATE THE ANALYSIS DATASET
# ============================================================================

print("\n2. Recreating analysis dataset...")
print("   Note: This requires access to the original data files.")
print("   The notebook uses Google Drive paths that are not available here.")
print("   Creating output templates based on notebook specifications...")

# Based on the notebook, the final analysis dataset has these variables:
dataset_variables = [
    'PERMNO',           # Company identifier
    'YEAR',             # Year
    'TICKER',           # Stock ticker
    'total_facilities', # Total number of facilities
    'num_disasters',    # Total disasters affecting facilities
    'exposed_facilities', # Number of facilities exposed to disasters
    'AFFECTED_RATIO',   # Proportion of facilities affected (key variable)
    'DISASTER',         # Binary indicator (1 if any disaster)
    'ROA',              # Return on Assets (dependent variable)
    'TOTAL_ASSETS',     # Total assets
    'NET_INCOME',       # Net income
    'TOTAL_DEBT',       # Total debt
    'TOTAL_REVENUE',    # Total revenue
    'LOG_ASSETS',       # Log of total assets (control)
    'LEVERAGE',         # Debt/Assets ratio (control)
    'REVENUE_GROWTH'    # Revenue growth rate (control)
]

# Create sample data structure description
dataset_description = {
    'Sample Period': '2016-2023',
    'Total Observations': '2,080 firm-years',
    'Unique Companies': '293 manufacturing firms',
    'Panel Structure': 'Unbalanced panel',
    'Key Variables': dataset_variables,
    'Data Sources': [
        'EPA Toxic Release Inventory (TRI) - facility locations',
        'SHELDUS - disaster events (2009-2023)',
        'CRSP - company identification',
        'Compustat - financial data'
    ]
}

# ============================================================================
# 3. STATISTICAL MODEL SPECIFICATION
# ============================================================================

print("\n3. Documenting statistical model specification...")

model_specification = """
STATISTICAL MODEL SPECIFICATION
================================

Primary Research Question:
-------------------------
Do natural disasters affecting a company's facilities impact its financial performance?

Dependent Variable:
------------------
ROA (Return on Assets) = Net Income / Total Assets
    - Measures firm profitability
    - Common financial performance metric
    - Ranges from negative (losses) to positive (profits)

Key Independent Variable:
------------------------
AFFECTED_RATIO = Number of Exposed Facilities / Total Facilities
    - Follows Hsu et al. (2018) methodology
    - Ranges from 0 (no exposure) to 1 (all facilities exposed)
    - A facility is "exposed" if a SHELDUS disaster event occurred in its FIPS county

Control Variables:
-----------------
1. LOG_ASSETS = ln(Total Assets)
   - Controls for firm size
   - Larger firms may have more resources to absorb shocks

2. LEVERAGE = Total Debt / Total Assets
   - Controls for financial structure
   - High leverage may amplify disaster impacts

3. Year Fixed Effects (Models 2-3)
   - Controls for time-varying macroeconomic conditions
   - Accounts for COVID-19 period effects (2020-2021)

Regression Models:
-----------------

Model 1: Simple OLS
    ROA_it = β₀ + β₁(AFFECTED_RATIO_it) + ε_it

Model 2: With Firm Controls
    ROA_it = β₀ + β₁(AFFECTED_RATIO_it) + β₂(LOG_ASSETS_it) 
           + β₃(LEVERAGE_it) + ε_it

Model 3: With Year Fixed Effects
    ROA_it = β₀ + β₁(AFFECTED_RATIO_it) + β₂(LOG_ASSETS_it) 
           + β₃(LEVERAGE_it) + Σγ_t(YEAR_t) + ε_it

Where:
    i = firm identifier
    t = year
    β₁ = coefficient of interest (disaster impact)
    ε_it = error term

Estimation Method:
-----------------
- Ordinary Least Squares (OLS) with robust standard errors
- Cross-sectional analysis (firm-year observations)
- No clustering (each firm-year treated as independent)

Sample Restrictions:
-------------------
1. Manufacturing firms only (based on SIC codes)
2. 2016-2023 period (ensures post-crisis data quality)
3. Non-missing financial data (ROA, assets, leverage)
4. Successfully matched TRI-CRSP-Compustat records

Hypothesis:
----------
H₀: β₁ = 0 (No effect of disasters on ROA)
H₁: β₁ < 0 (Disasters negatively impact ROA)

Expected Sign: Negative
    - Disasters disrupt operations
    - Increase costs (repairs, insurance deductibles)
    - Reduce productivity
    
Actual Finding: β₁ ≈ 0 (null result)
    - Suggests manufacturing firms are resilient
    - May have insurance, geographic diversification
    - Contrasts with Hsu et al.'s broader sample results
"""

# ============================================================================
# 4. DESCRIPTIVE STATISTICS (from notebook output)
# ============================================================================

print("\n4. Creating descriptive statistics table...")

# Based on notebook cell output
descriptive_stats = {
    'Variable': [
        'AFFECTED_RATIO',
        'DISASTER', 
        'num_disasters',
        'total_facilities',
        'ROA',
        'TOTAL_ASSETS',
        'LEVERAGE'
    ],
    'N': [2123, 2123, 2123, 2123, 2080, 2080, 2080],
    'Mean': [0.240172, 0.506830, 2887.606689, 36.739520, 0.054731, 20312.067044, 0.313377],
    'Std Dev': [0.320174, 0.500071, 31010.629706, 111.925759, 0.085340, 39666.992610, 0.160888],
    'Min': [0.000000, 0.000000, 0.000000, 1.000000, -0.759072, 0.352000, 0.000000],
    '25%': [0.000000, 0.000000, 0.000000, 3.000000, 0.022860, 1760.200000, 0.216307],
    '50%': [0.038462, 1.000000, 2.000000, 10.000000, 0.052336, 5543.850000, 0.310724],
    '75%': [0.400000, 1.000000, 110.000000, 26.000000, 0.087537, 20184.050000, 0.404490],
    'Max': [1.000000, 1.000000, 557184.000000, 1495.000000, 1.495879, 376317.000000, 1.210120]
}

descriptive_stats_df = pd.DataFrame(descriptive_stats)

# Exposure distribution details
exposure_distribution = {
    'Exposure Level': [
        'No exposure (0%)',
        'Low exposure (1-25%)',
        'Medium exposure (26-50%)',
        'High exposure (51-75%)',
        'Very high exposure (76-100%)'
    ],
    'N': [1047, 330, 349, 169, 228],
    'Percentage': [49.3, 15.5, 16.4, 8.0, 10.7]
}

exposure_df = pd.DataFrame(exposure_distribution)

# ============================================================================
# 5. CORRELATION MATRIX
# ============================================================================

print("\n5. Creating correlation matrix...")

# Based on typical correlations for these variables
# Note: These should be calculated from actual data, but we provide structure
correlation_vars = [
    'ROA', 'AFFECTED_RATIO', 'LOG_ASSETS', 'LEVERAGE', 
    'num_disasters', 'total_facilities'
]

# Create template correlation matrix structure
correlation_matrix_template = pd.DataFrame(
    index=correlation_vars,
    columns=correlation_vars,
    dtype=float
)

# Note about correlations
correlation_note = """
CORRELATION MATRIX NOTES:
------------------------
The correlation matrix should be calculated from the actual analysis dataset.
This requires access to the complete merged data with all 2,080 observations.

Key relationships to examine:
1. ROA vs AFFECTED_RATIO - Main relationship of interest
2. LOG_ASSETS vs ROA - Size effect on profitability
3. LEVERAGE vs ROA - Financial structure effect
4. AFFECTED_RATIO vs total_facilities - Exposure patterns by firm size
5. Multicollinearity among controls

Expected patterns:
- AFFECTED_RATIO vs ROA: Near-zero (based on null finding)
- LOG_ASSETS vs ROA: Positive (larger firms more profitable)
- LEVERAGE vs ROA: Negative (debt reduces profitability)
- LOG_ASSETS vs LEVERAGE: Positive (larger firms carry more debt)
"""

# ============================================================================
# 6. REGRESSION RESULTS (from notebook output)
# ============================================================================

print("\n6. Formatting regression results...")

# Model 1: Simple OLS
model1_results = {
    'Variable': ['Intercept', 'AFFECTED_RATIO'],
    'Coefficient': [0.0551, -0.0016],
    'Std Error': [0.002, 0.006],
    't-statistic': [23.542, -0.266],
    'P-value': [0.000, 0.790],
    '95% CI Lower': [0.051, -0.013],
    '95% CI Upper': [0.060, 0.010]
}
model1_df = pd.DataFrame(model1_results)
model1_stats = {
    'N': 2080,
    'R-squared': 0.000,
    'Adj. R-squared': -0.000,
    'F-statistic': 0.071,
    'Prob (F-statistic)': 0.790
}

# Model 2: With Controls
model2_results = {
    'Variable': ['Intercept', 'AFFECTED_RATIO', 'LOG_ASSETS', 'LEVERAGE'],
    'Coefficient': [0.0360, -0.0009, 0.0057, -0.0971],
    'Std Error': [0.010, 0.006, 0.001, 0.012],
    't-statistic': [3.710, -0.161, 5.260, -8.332],
    'P-value': [0.000, 0.872, 0.000, 0.000],
    '95% CI Lower': [0.017, -0.012, 0.004, -0.120],
    '95% CI Upper': [0.055, 0.010, 0.008, -0.074]
}
model2_df = pd.DataFrame(model2_results)
model2_stats = {
    'N': 2080,
    'R-squared': 0.038,
    'Adj. R-squared': 0.037,
    'F-statistic': 27.65,
    'Prob (F-statistic)': 1.57e-17
}

# Model 3: With Year Fixed Effects
model3_results = {
    'Variable': [
        'Intercept', 
        'AFFECTED_RATIO', 
        'LOG_ASSETS', 
        'LEVERAGE',
        'Year 2017',
        'Year 2018',
        'Year 2019',
        'Year 2020',
        'Year 2021',
        'Year 2022',
        'Year 2023'
    ],
    'Coefficient': [
        0.0333, 0.0042, 0.0055, -0.0970,
        -0.0013, 0.0042, -0.0007, -0.0132,
        0.0173, 0.0164, 0.0007
    ],
    'Std Error': [
        0.011, 0.006, 0.001, 0.012,
        0.007, 0.007, 0.007, 0.007,
        0.007, 0.008, 0.008
    ],
    't-statistic': [
        3.126, 0.665, 5.112, -8.347,
        -0.176, 0.570, -0.101, -1.792,
        2.347, 2.153, 0.093
    ],
    'P-value': [
        0.002, 0.506, 0.000, 0.000,
        0.860, 0.568, 0.920, 0.073,
        0.019, 0.031, 0.926
    ],
    '95% CI Lower': [
        0.012, -0.008, 0.003, -0.120,
        -0.016, -0.010, -0.015, -0.028,
        0.003, 0.001, -0.014
    ],
    '95% CI Upper': [
        0.054, 0.017, 0.008, -0.074,
        0.013, 0.019, 0.014, 0.001,
        0.032, 0.031, 0.016
    ]
}
model3_df = pd.DataFrame(model3_results)
model3_stats = {
    'N': 2080,
    'R-squared': 0.050,
    'Adj. R-squared': 0.045,
    'F-statistic': 10.88,
    'Prob (F-statistic)': 3.07e-18
}

# Summary comparison table
regression_summary = {
    'Model': ['(1) Simple', '(2) Controls', '(3) Year FE'],
    'Coefficient': [-0.001555, -0.000923, 0.004226],
    'Std Error': [0.005836, 0.005735, 0.006356],
    'P-value': [0.789982, 0.872152, 0.506188],
    'R-squared': [0.000034, 0.038420, 0.049951],
    'N': [2080, 2080, 2080]
}
regression_summary_df = pd.DataFrame(regression_summary)

# ============================================================================
# 7. SAVE ALL OUTPUTS TO 2 CONSOLIDATED FILES
# ============================================================================

print("\n7. Creating consolidated output files (2 files only)...")

output_dir = Path('statistical_analysis_outputs')
output_dir.mkdir(exist_ok=True)

# Track file creation success
files_created = []
files_failed = []

# ============================================================================
# FILE 1: COMPLETE_DATA.xlsx - All data-related information
# ============================================================================
print("\n   Creating COMPLETE_DATA.xlsx...")

data_file = output_dir / 'COMPLETE_DATA.xlsx'

try:
    with pd.ExcelWriter(data_file, engine='openpyxl') as writer:
        # Sheet 1: Analysis Dataset Description
        dataset_desc_text = []
        dataset_desc_text.append("ANALYSIS DATASET DESCRIPTION")
        dataset_desc_text.append("="*80)
        dataset_desc_text.append("")
        dataset_desc_text.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dataset_desc_text.append("")
        for key, value in dataset_description.items():
            dataset_desc_text.append(f"{key}:")
            if isinstance(value, list):
                for item in value:
                    dataset_desc_text.append(f"  - {item}")
            else:
                dataset_desc_text.append(f"  {value}")
            dataset_desc_text.append("")
        
        dataset_desc_text.append("IMPORTANT NOTE:")
        dataset_desc_text.append("-" * 80)
        dataset_desc_text.append("To generate the complete dataset with all 2,080 observations:")
        dataset_desc_text.append("1. Run the Jupyter notebooks in sequence (Notebooks 1-5)")
        dataset_desc_text.append("2. The notebooks require access to the Google Drive data files")
        dataset_desc_text.append("3. Final dataset is created in Notebook 5 after merging:")
        dataset_desc_text.append("   - TRI facility data")
        dataset_desc_text.append("   - SHELDUS disaster events")
        dataset_desc_text.append("   - CRSP company matching")
        dataset_desc_text.append("   - Compustat financial data")
        
        dataset_desc_df = pd.DataFrame({'Dataset Description': dataset_desc_text})
        dataset_desc_df.to_excel(writer, sheet_name='Dataset_Description', index=False)
        
        # Sheet 2: Descriptive Statistics
        descriptive_stats_df.to_excel(writer, sheet_name='Descriptive_Statistics', index=False)
        
        # Sheet 3: Data Dictionary
        data_dict_vars = ['PERMNO', 'YEAR', 'TICKER', 'total_facilities', 'num_disasters',
                         'exposed_facilities', 'AFFECTED_RATIO', 'DISASTER', 'ROA',
                         'TOTAL_ASSETS', 'NET_INCOME', 'TOTAL_DEBT', 'TOTAL_REVENUE',
                         'LOG_ASSETS', 'LEVERAGE', 'REVENUE_GROWTH']
        data_dict_descriptions = [
            'CRSP permanent company identifier',
            'Fiscal year (2016-2023)',
            'Stock ticker symbol',
            'Total number of TRI-registered facilities',
            'Total count of SHELDUS disaster events affecting facilities',
            'Number of facilities in disaster-affected counties',
            'Proportion of facilities exposed to disasters (0-1)',
            'Binary indicator: 1 if any facility exposed to disaster',
            'Return on Assets = Net Income / Total Assets (dependent variable)',
            'Total assets in millions USD',
            'Net income in millions USD',
            'Total debt in millions USD',
            'Total revenue in millions USD',
            'Natural logarithm of total assets (size control)',
            'Financial leverage = Total Debt / Total Assets (control)',
            'Revenue growth rate (control)'
        ]
        data_dictionary_df = pd.DataFrame({
            'Variable': data_dict_vars,
            'Description': data_dict_descriptions
        })
        data_dictionary_df.to_excel(writer, sheet_name='Data_Dictionary', index=False)
        
        # Sheet 4: Exposure Distribution
        exposure_df.to_excel(writer, sheet_name='Exposure_Distribution', index=False)
        
        # Sheet 5: Yearly Statistics (sample structure)
        # Define years from dataset description
        years_range = list(range(2016, 2024))  # 2016-2023
        yearly_stats_data = {
            'Year': years_range,
            'Note': ['Run notebooks to generate actual yearly statistics'] * len(years_range)
        }
        yearly_stats_df = pd.DataFrame(yearly_stats_data)
        yearly_stats_df.to_excel(writer, sheet_name='Yearly_Statistics', index=False)
    
    print(f"   ✓ Saved: {data_file}")
    print(f"      - Sheet 1: Dataset_Description")
    print(f"      - Sheet 2: Descriptive_Statistics")
    print(f"      - Sheet 3: Data_Dictionary")
    print(f"      - Sheet 4: Exposure_Distribution")
    print(f"      - Sheet 5: Yearly_Statistics")
    files_created.append('COMPLETE_DATA.xlsx')

except ImportError as e:
    print(f"   ✗ ERROR: openpyxl not available")
    print(f"      Install with: pip install openpyxl")
    files_failed.append('COMPLETE_DATA.xlsx')
except Exception as e:
    print(f"   ✗ ERROR creating COMPLETE_DATA.xlsx: {e}")
    files_failed.append('COMPLETE_DATA.xlsx')

# ============================================================================
# FILE 2: COMPLETE_RESULTS.xlsx - All statistical results
# ============================================================================
print("\n   Creating COMPLETE_RESULTS.xlsx...")

results_file = output_dir / 'COMPLETE_RESULTS.xlsx'

try:
    with pd.ExcelWriter(results_file, engine='openpyxl') as writer:
        # Sheet 1: Model Specification
        model_spec_lines = model_specification.strip().split('\n')
        model_spec_df = pd.DataFrame({'Model Specification': model_spec_lines})
        model_spec_df.to_excel(writer, sheet_name='Model_Specification', index=False)
        
        # Sheet 2: Correlation Matrix Note
        corr_note_lines = correlation_note.strip().split('\n')
        corr_note_df = pd.DataFrame({'Correlation Matrix Notes': corr_note_lines})
        corr_note_df.to_excel(writer, sheet_name='Correlation_Matrix_Notes', index=False)
        
        # Sheet 3: Model 1 Results
        model1_df.to_excel(writer, sheet_name='Model1_Simple_OLS', index=False)
        
        # Add model 1 statistics as separate rows
        model1_stats_df = pd.DataFrame([
            ['', ''],
            ['Model Statistics:', ''],
            ['N', model1_stats['N']],
            ['R-squared', model1_stats['R-squared']],
            ['Adj. R-squared', model1_stats['Adj. R-squared']],
            ['F-statistic', model1_stats['F-statistic']],
            ['Prob (F-statistic)', model1_stats['Prob (F-statistic)']]
        ], columns=['Statistic', 'Value'])
        model1_stats_df.to_excel(writer, sheet_name='Model1_Statistics', index=False)
        
        # Sheet 4: Model 2 Results
        model2_df.to_excel(writer, sheet_name='Model2_With_Controls', index=False)
        
        model2_stats_df = pd.DataFrame([
            ['', ''],
            ['Model Statistics:', ''],
            ['N', model2_stats['N']],
            ['R-squared', model2_stats['R-squared']],
            ['Adj. R-squared', model2_stats['Adj. R-squared']],
            ['F-statistic', model2_stats['F-statistic']],
            ['Prob (F-statistic)', model2_stats['Prob (F-statistic)']]
        ], columns=['Statistic', 'Value'])
        model2_stats_df.to_excel(writer, sheet_name='Model2_Statistics', index=False)
        
        # Sheet 5: Model 3 Results
        model3_df.to_excel(writer, sheet_name='Model3_Year_FE', index=False)
        
        model3_stats_df = pd.DataFrame([
            ['', ''],
            ['Model Statistics:', ''],
            ['N', model3_stats['N']],
            ['R-squared', model3_stats['R-squared']],
            ['Adj. R-squared', model3_stats['Adj. R-squared']],
            ['F-statistic', model3_stats['F-statistic']],
            ['Prob (F-statistic)', model3_stats['Prob (F-statistic)']]
        ], columns=['Statistic', 'Value'])
        model3_stats_df.to_excel(writer, sheet_name='Model3_Statistics', index=False)
        
        # Sheet 6: Regression Summary Table
        regression_summary_df.to_excel(writer, sheet_name='Regression_Summary', index=False)
        
        # Sheet 7: Publication-Ready Table
        # Use dictionary-based lookup instead of hard-coded indices
        pub_table_data = []
        pub_table_data.append(['Variable', 'Model 1', 'Model 2', 'Model 3'])
        
        # Helper function to safely get coefficient by variable name
        def get_coef(model_results, var_name, stat='Coefficient'):
            """Safely retrieve coefficient by variable name"""
            var_list = model_results.get('Variable', [])
            if var_name in var_list:
                idx = var_list.index(var_name)
                return model_results[stat][idx]
            return None
        
        # AFFECTED_RATIO row
        pub_table_data.append(['AFFECTED_RATIO', 
                              f"{get_coef(model1_results, 'AFFECTED_RATIO'):.4f}",
                              f"{get_coef(model2_results, 'AFFECTED_RATIO'):.4f}",
                              f"{get_coef(model3_results, 'AFFECTED_RATIO'):.4f}"])
        pub_table_data.append(['', 
                              f"({get_coef(model1_results, 'AFFECTED_RATIO', 'Std Error'):.4f})",
                              f"({get_coef(model2_results, 'AFFECTED_RATIO', 'Std Error'):.4f})",
                              f"({get_coef(model3_results, 'AFFECTED_RATIO', 'Std Error'):.4f})"])
        
        # LOG_ASSETS row (only in models 2 and 3)
        pub_table_data.append(['LOG_ASSETS', '', 
                              f"{get_coef(model2_results, 'LOG_ASSETS'):.4f}",
                              f"{get_coef(model3_results, 'LOG_ASSETS'):.4f}"])
        pub_table_data.append(['', '', 
                              f"({get_coef(model2_results, 'LOG_ASSETS', 'Std Error'):.4f})",
                              f"({get_coef(model3_results, 'LOG_ASSETS', 'Std Error'):.4f})"])
        
        # LEVERAGE row (only in models 2 and 3)
        pub_table_data.append(['LEVERAGE', '', 
                              f"{get_coef(model2_results, 'LEVERAGE'):.4f}",
                              f"{get_coef(model3_results, 'LEVERAGE'):.4f}"])
        pub_table_data.append(['', '', 
                              f"({get_coef(model2_results, 'LEVERAGE', 'Std Error'):.4f})",
                              f"({get_coef(model3_results, 'LEVERAGE', 'Std Error'):.4f})"])
        
        pub_table_data.append(['', '', '', ''])
        pub_table_data.append(['Year Fixed Effects', 'No', 'No', 'Yes'])
        pub_table_data.append(['N', model1_stats['N'], model2_stats['N'], model3_stats['N']])
        pub_table_data.append(['R-squared', 
                              f"{model1_stats['R-squared']:.4f}",
                              f"{model2_stats['R-squared']:.4f}",
                              f"{model3_stats['R-squared']:.4f}"])
        
        pub_table_df = pd.DataFrame(pub_table_data)
        pub_table_df.to_excel(writer, sheet_name='Publication_Table', index=False, header=False)
    
    print(f"   ✓ Saved: {results_file}")
    print(f"      - Sheet 1: Model_Specification")
    print(f"      - Sheet 2: Correlation_Matrix_Notes")
    print(f"      - Sheet 3: Model1_Simple_OLS")
    print(f"      - Sheet 4: Model1_Statistics")
    print(f"      - Sheet 5: Model2_With_Controls")
    print(f"      - Sheet 6: Model2_Statistics")
    print(f"      - Sheet 7: Model3_Year_FE")
    print(f"      - Sheet 8: Model3_Statistics")
    print(f"      - Sheet 9: Regression_Summary")
    print(f"      - Sheet 10: Publication_Table")
    files_created.append('COMPLETE_RESULTS.xlsx')

except ImportError as e:
    print(f"   ✗ ERROR: openpyxl not available")
    print(f"      Install with: pip install openpyxl")
    files_failed.append('COMPLETE_RESULTS.xlsx')
except Exception as e:
    print(f"   ✗ ERROR creating COMPLETE_RESULTS.xlsx: {e}")
    files_failed.append('COMPLETE_RESULTS.xlsx')

# ============================================================================
# 8. CREATE SUMMARY README
# ============================================================================

print("\n8. Creating summary README...")

summary_doc = f"""
STATISTICAL ANALYSIS - CONSOLIDATED OUTPUT
===========================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
For: Professor Yanjie Yang

OUTPUT FILES (2 FILES ONLY)
---------------------------

📊 **COMPLETE_DATA.xlsx** - All data-related information
   Contains 5 sheets:
   1. Dataset_Description - Overview of the analysis dataset
   2. Descriptive_Statistics - Summary statistics for all variables
   3. Data_Dictionary - Variable definitions and descriptions
   4. Exposure_Distribution - Distribution of disaster exposure levels
   5. Yearly_Statistics - Year-by-year summary (template)

📈 **COMPLETE_RESULTS.xlsx** - All statistical results
   Contains 10 sheets:
   1. Model_Specification - Research question and model equations
   2. Correlation_Matrix_Notes - Instructions for correlation analysis
   3. Model1_Simple_OLS - Model 1 regression coefficients
   4. Model1_Statistics - Model 1 fit statistics
   5. Model2_With_Controls - Model 2 regression coefficients
   6. Model2_Statistics - Model 2 fit statistics
   7. Model3_Year_FE - Model 3 regression coefficients (main specification)
   8. Model3_Statistics - Model 3 fit statistics
   9. Regression_Summary - Comparison of all three models
   10. Publication_Table - Publication-ready results table

KEY FINDINGS (Hsu et al. 2018 Methodology)
------------------------------------------
✓ NULL RESULT: Disasters do not significantly affect ROA in manufacturing firms
✓ Coefficient near zero across all specifications
✓ P-values > 0.50 in all models (not statistically significant)
✓ Control variables work as expected (size positive, leverage negative)
✓ Robust to model specification

Model 1 (Simple OLS):     β = -0.0016, p = 0.790, R² = 0.000
Model 2 (With Controls):  β = -0.0009, p = 0.872, R² = 0.038
Model 3 (Year FE - Main): β = +0.0042, p = 0.506, R² = 0.050

INTERPRETATION
--------------
Manufacturing firms appear resilient to disaster exposure, likely due to:
- Insurance coverage
- Geographic diversification  
- Supply chain flexibility
- Asset fungibility

This contrasts with Hsu et al. (2018) findings for broader samples,
suggesting manufacturing sector has unique resilience characteristics.

DATA SOURCES
------------
- TRI (Toxic Release Inventory) - Facility locations
- SHELDUS - Disaster events (2009-2023)
- CRSP - Company identification
- Compustat - Financial data

Sample: 2,080 firm-years, 293 manufacturing firms, 2016-2023

METHODOLOGY REFERENCE
---------------------
Hsu, P. H., Li, X., & Moore, J. A. (2018). 
"Exploring the impact of disasters on firm value"
Specification: Lagged disaster exposure (t-1) predicts ROA (t)

NOTEBOOKS AVAILABLE
-------------------
For complete data generation and robustness checks:
- Data_Preparation_FIPS.ipynb
- Automated_Matching_FIPS.ipynb
- 03_manual_review_and_analysis.ipynb
- 04_disaster_exposure_analysis.ipynb
- 05_CLEAN_affected_ratio_baseline_regression.ipynb
- 06_ROBUSTNESS_CHECKS_CLEAN.ipynb
- 07_Generate_Statistical_Outputs.ipynb
- 08_FINAL_CONSOLIDATED_OUTPUTS.ipynb (generates these 2 files)

CONTACT
-------
Student: Apoorv Saxena (s1129420@mail.yzu.edu.tw)
Supervisor: Professor Yanjie Yang (yanjie@saturn.yzu.edu.tw)
Yuan Ze University, December 2025
"""

with open(output_dir / 'README.txt', 'w') as f:
    f.write(summary_doc)

print(f"   ✓ Saved: {output_dir / 'README.txt'}")
files_created.append('README.txt')

# ============================================================================
# 9. COMPLETION
# ============================================================================

print("\n" + "="*80)
print("GENERATION COMPLETE - CONSOLIDATED OUTPUT (2 FILES)")
print("="*80)
print(f"\nAll outputs saved to: {output_dir}/")

# Show status of file creation
if files_created:
    print("\nFiles successfully created:")
    for file_name in files_created:
        file_path = output_dir / file_name
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"  ✓ {file_name} ({size:,} bytes)")
        else:
            print(f"  ✓ {file_name}")

if files_failed:
    print("\n⚠️  Files that could not be created:")
    for file_name in files_failed:
        print(f"  ✗ {file_name}")

print("\n" + "="*80)
if len(files_failed) == 0:
    print("✅ SUCCESS - All Files Generated!")
    print("="*80)
    print("""
✅ COMPLETE_DATA.xlsx    - All data-related information (5 sheets)
✅ COMPLETE_RESULTS.xlsx - All statistical results (10 sheets)
✅ README.txt            - Summary and instructions

Next Steps:
1. Review both Excel files to verify all information is present
2. Share COMPLETE_DATA.xlsx and COMPLETE_RESULTS.xlsx with Professor Yang
3. To generate actual dataset: Run Notebooks 1-5 in sequence
4. For robustness checks: See Notebook 6
""")
else:
    print("⚠️  PARTIAL SUCCESS - Some Files Could Not Be Created")
    print("="*80)
    print(f"\nSuccessfully created {len(files_created)} of {len(files_created) + len(files_failed)} files")
    print("\nPlease install missing dependencies:")
    print("  pip install openpyxl pandas numpy")
    print("")
    sys.exit(1)  # Exit with error code

print("\n✓ Script completed successfully")
sys.exit(0)  # Exit with success code
