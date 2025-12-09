#!/usr/bin/env python3
"""
⚠️ DEPRECATION NOTICE
=====================
This script has been superseded by the consolidated output approach.

Please use instead:
- generate_statistical_outputs.py (for 2-file consolidated output)
- 08_FINAL_CONSOLIDATED_OUTPUTS.ipynb (same 2-file output in notebook format)

These create only 2 files:
- COMPLETE_DATA.xlsx (all data in 5 sheets)
- COMPLETE_RESULTS.xlsx (all results in 10 sheets)

This file is kept for reference but is no longer actively maintained.

---

Data Export Script for Statistical Analysis (LEGACY)
====================================================
This script should be run AFTER Notebook 5 has been executed.
It exports the complete analysis dataset and correlation matrix.

Add this to the end of Notebook 5 to generate the required files.

Usage in Jupyter Notebook:
    # After running all cells in Notebook 5, add this as a new cell:
    %run export_dataset_and_correlation.py

Or run standalone:
    python3 export_dataset_and_correlation.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("="*80)
print("EXPORTING COMPLETE ANALYSIS DATASET AND CORRELATION MATRIX")
print("="*80)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directory
OUTPUT_DIR = Path('statistical_analysis_outputs')
OUTPUT_DIR.mkdir(exist_ok=True)

# This assumes the notebook variables are in scope
# If running standalone, you'll need to load the data first

# ============================================================================
# 1. EXPORT COMPLETE ANALYSIS DATASET
# ============================================================================

print("\n1. Exporting complete analysis dataset...")

try:
    # This variable should exist after running Notebook 5
    if 'analysis_data' not in globals():
        print("   ERROR: 'analysis_data' DataFrame not found!")
        print("   Please run Notebook 5 first to create the analysis dataset.")
    else:
        # Select all relevant columns
        export_columns = [
            'PERMNO',           # Company identifier
            'YEAR',             # Year
            'TICKER',           # Stock ticker
            'total_facilities', # Total facilities
            'num_disasters',    # Total disasters
            'exposed_facilities', # Facilities exposed
            'AFFECTED_RATIO',   # Key independent variable
            'DISASTER',         # Binary disaster indicator
            'ROA',              # Dependent variable
            'TOTAL_ASSETS',     # Financial data
            'NET_INCOME',
            'TOTAL_DEBT',
            'TOTAL_REVENUE',
            'LOG_ASSETS',       # Control variable
            'LEVERAGE',         # Control variable
            'REVENUE_GROWTH'    # Control variable (if exists)
        ]
        
        # Only include columns that exist
        existing_columns = [col for col in export_columns if col in analysis_data.columns]
        
        # Export the dataset
        dataset_export = analysis_data[existing_columns].copy()
        
        # Sort by company and year for clarity
        if 'PERMNO' in dataset_export.columns and 'YEAR' in dataset_export.columns:
            dataset_export = dataset_export.sort_values(['PERMNO', 'YEAR'])
        
        # Save in multiple formats
        csv_file = OUTPUT_DIR / 'COMPLETE_ANALYSIS_DATASET.csv'
        xlsx_file = OUTPUT_DIR / 'COMPLETE_ANALYSIS_DATASET.xlsx'
        
        dataset_export.to_csv(csv_file, index=False)
        dataset_export.to_excel(xlsx_file, index=False, engine='openpyxl')
        
        print(f"   ✓ Saved: {csv_file}")
        print(f"   ✓ Saved: {xlsx_file}")
        print(f"   ✓ Shape: {dataset_export.shape[0]:,} rows × {dataset_export.shape[1]} columns")
        print(f"   ✓ Companies: {dataset_export['PERMNO'].nunique():,}")
        print(f"   ✓ Years: {dataset_export['YEAR'].min()}-{dataset_export['YEAR'].max()}")
        
        # Create data dictionary
        data_dict = []
        for col in existing_columns:
            non_null = dataset_export[col].notna().sum()
            data_type = str(dataset_export[col].dtype)
            
            if dataset_export[col].dtype in ['float64', 'int64']:
                mean_val = dataset_export[col].mean()
                std_val = dataset_export[col].std()
                min_val = dataset_export[col].min()
                max_val = dataset_export[col].max()
                desc = f"Mean={mean_val:.4f}, Std={std_val:.4f}, Min={min_val:.4f}, Max={max_val:.4f}"
            else:
                unique_vals = dataset_export[col].nunique()
                desc = f"{unique_vals} unique values"
            
            data_dict.append({
                'Variable': col,
                'Type': data_type,
                'Non-Missing': non_null,
                'Description': desc
            })
        
        data_dict_df = pd.DataFrame(data_dict)
        dict_file = OUTPUT_DIR / 'DATA_DICTIONARY.csv'
        data_dict_df.to_csv(dict_file, index=False)
        print(f"   ✓ Saved: {dict_file}")
        
except Exception as e:
    print(f"   ERROR: {e}")
    print("   Make sure you've run all cells in Notebook 5 first.")

# ============================================================================
# 2. CALCULATE AND EXPORT CORRELATION MATRIX
# ============================================================================

print("\n2. Calculating correlation matrix...")

try:
    if 'analysis_data' not in globals():
        print("   ERROR: 'analysis_data' DataFrame not found!")
    else:
        # Select numeric variables for correlation
        corr_vars = [
            'ROA',
            'AFFECTED_RATIO',
            'LOG_ASSETS',
            'LEVERAGE',
            'num_disasters',
            'total_facilities',
            'exposed_facilities'
        ]
        
        # Add REVENUE_GROWTH if it exists
        if 'REVENUE_GROWTH' in analysis_data.columns:
            corr_vars.append('REVENUE_GROWTH')
        
        # Only include variables that exist
        corr_vars = [v for v in corr_vars if v in analysis_data.columns]
        
        # Calculate correlation matrix
        correlation_matrix = analysis_data[corr_vars].corr()
        
        # Save correlation matrix
        corr_csv = OUTPUT_DIR / '04_CORRELATION_MATRIX.csv'
        corr_xlsx = OUTPUT_DIR / '04_CORRELATION_MATRIX.xlsx'
        
        correlation_matrix.to_csv(corr_csv)
        correlation_matrix.to_excel(corr_xlsx, engine='openpyxl')
        
        print(f"   ✓ Saved: {corr_csv}")
        print(f"   ✓ Saved: {corr_xlsx}")
        print(f"   ✓ Variables included: {len(corr_vars)}")
        
        # Print correlation matrix
        print("\n   Correlation Matrix:")
        print("   " + "-"*70)
        pd.set_option('display.precision', 3)
        pd.set_option('display.width', 120)
        print(correlation_matrix.to_string())
        
        # Highlight key correlations
        print("\n   Key Correlations:")
        print("   " + "-"*70)
        
        if 'ROA' in correlation_matrix.index and 'AFFECTED_RATIO' in correlation_matrix.columns:
            roa_affected = correlation_matrix.loc['ROA', 'AFFECTED_RATIO']
            print(f"   ROA vs AFFECTED_RATIO: {roa_affected:.4f}")
        
        if 'ROA' in correlation_matrix.index and 'LOG_ASSETS' in correlation_matrix.columns:
            roa_size = correlation_matrix.loc['ROA', 'LOG_ASSETS']
            print(f"   ROA vs LOG_ASSETS: {roa_size:.4f}")
        
        if 'ROA' in correlation_matrix.index and 'LEVERAGE' in correlation_matrix.columns:
            roa_lev = correlation_matrix.loc['ROA', 'LEVERAGE']
            print(f"   ROA vs LEVERAGE: {roa_lev:.4f}")
        
        if 'LOG_ASSETS' in correlation_matrix.index and 'LEVERAGE' in correlation_matrix.columns:
            size_lev = correlation_matrix.loc['LOG_ASSETS', 'LEVERAGE']
            print(f"   LOG_ASSETS vs LEVERAGE: {size_lev:.4f}")
        
except Exception as e:
    print(f"   ERROR: {e}")
    print("   Make sure you've run all cells in Notebook 5 first.")

# ============================================================================
# 3. SUMMARY STATISTICS BY EXPOSURE GROUP
# ============================================================================

print("\n3. Creating summary statistics by exposure group...")

try:
    if 'analysis_data' not in globals():
        print("   ERROR: 'analysis_data' DataFrame not found!")
    else:
        # Create exposure groups
        analysis_data_copy = analysis_data.copy()
        
        conditions = [
            (analysis_data_copy['AFFECTED_RATIO'] == 0),
            ((analysis_data_copy['AFFECTED_RATIO'] > 0) & (analysis_data_copy['AFFECTED_RATIO'] <= 0.25)),
            ((analysis_data_copy['AFFECTED_RATIO'] > 0.25) & (analysis_data_copy['AFFECTED_RATIO'] <= 0.50)),
            ((analysis_data_copy['AFFECTED_RATIO'] > 0.50) & (analysis_data_copy['AFFECTED_RATIO'] <= 0.75)),
            (analysis_data_copy['AFFECTED_RATIO'] > 0.75)
        ]
        
        labels = ['No Exposure', 'Low (1-25%)', 'Medium (26-50%)', 'High (51-75%)', 'Very High (76-100%)']
        
        analysis_data_copy['Exposure_Group'] = np.select(conditions, labels, default='Unknown')
        
        # Summary by group
        if 'ROA' in analysis_data_copy.columns:
            summary_by_group = analysis_data_copy.groupby('Exposure_Group').agg({
                'ROA': ['count', 'mean', 'std', 'min', 'max'],
                'TOTAL_ASSETS': ['mean', 'std'],
                'LEVERAGE': ['mean', 'std']
            }).round(4)
            
            summary_file = OUTPUT_DIR / 'SUMMARY_BY_EXPOSURE_GROUP.csv'
            summary_by_group.to_csv(summary_file)
            print(f"   ✓ Saved: {summary_file}")
            
            print("\n   Summary by Exposure Group:")
            print("   " + "-"*70)
            print(summary_by_group.to_string())
        
except Exception as e:
    print(f"   ERROR: {e}")

# ============================================================================
# COMPLETION
# ============================================================================

print("\n" + "="*80)
print("EXPORT COMPLETE")
print("="*80)
print("\nAll files saved to:", OUTPUT_DIR)
print("\nFiles that should now exist:")
print("  - COMPLETE_ANALYSIS_DATASET.csv (main deliverable)")
print("  - COMPLETE_ANALYSIS_DATASET.xlsx")
print("  - DATA_DICTIONARY.csv")
print("  - 04_CORRELATION_MATRIX.csv (main deliverable)")
print("  - 04_CORRELATION_MATRIX.xlsx")
print("  - SUMMARY_BY_EXPOSURE_GROUP.csv")
print("\n✓ Ready to send to Professor Yang")
