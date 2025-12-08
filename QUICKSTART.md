# Quick Start Guide: Generating Statistical Outputs for Professor Yang

This guide explains how to provide Professor Yang with all the requested statistical analysis outputs.

## What Professor Yang Requested

1. ✅ All observations used in statistical analysis (combined in a single file)
2. ✅ Statistical model specification
3. ✅ Descriptive statistics of the variables
4. ✅ Correlation matrix of the variables
5. ✅ Regression output tables (including coefficients of all variables)

## Already Generated (Ready to Use)

All files in the `statistical_analysis_outputs/` folder are ready to send to Professor Yang:

- **Model Specification**: `02_STATISTICAL_MODEL.txt`
- **Descriptive Statistics**: `03_DESCRIPTIVE_STATISTICS.xlsx`
- **Exposure Distribution**: `03b_EXPOSURE_DISTRIBUTION.xlsx`
- **Regression Results**: `05a`, `05b`, `05c`, `05d` files (all models with coefficients)
- **Summary Document**: `00_README.txt`

## Still Need to Generate

Two items require running the notebooks with actual data:

### 1. Complete Analysis Dataset (2,080 observations)
### 2. Correlation Matrix

## How to Generate Missing Items

### Step-by-Step Instructions:

1. **Open Google Colab and run Notebook 5:**
   ```
   05_CLEAN_affected_ratio_baseline_regression.ipynb
   ```

2. **After all cells have executed successfully, add a new cell at the end:**
   ```python
   # Download the export script if not already in the notebook directory
   !wget https://raw.githubusercontent.com/ApoorvSaxena0109/data-synthesizer/main/export_dataset_and_correlation.py
   
   # Run the export script
   %run export_dataset_and_correlation.py
   ```

3. **The script will generate:**
   - `COMPLETE_ANALYSIS_DATASET.csv` (2,080 rows × 16 columns)
   - `COMPLETE_ANALYSIS_DATASET.xlsx`
   - `04_CORRELATION_MATRIX.csv`
   - `04_CORRELATION_MATRIX.xlsx`
   - `DATA_DICTIONARY.csv`
   - `SUMMARY_BY_EXPOSURE_GROUP.csv`

4. **Download the generated files** from the Colab environment to your local machine

## Alternative: Manual Export from Notebook 5

If you prefer to do it manually, add this code at the end of Notebook 5:

```python
# Export complete dataset
output_dir = Path('statistical_analysis_outputs')
output_dir.mkdir(exist_ok=True)

# 1. Export the complete analysis dataset
columns_to_export = [
    'PERMNO', 'YEAR', 'TICKER', 
    'total_facilities', 'num_disasters', 'exposed_facilities',
    'AFFECTED_RATIO', 'DISASTER',
    'ROA', 'TOTAL_ASSETS', 'NET_INCOME', 'TOTAL_DEBT', 'TOTAL_REVENUE',
    'LOG_ASSETS', 'LEVERAGE', 'REVENUE_GROWTH'
]

# Filter to existing columns
existing_cols = [c for c in columns_to_export if c in analysis_data.columns]
dataset_export = analysis_data[existing_cols].copy()

# Save
dataset_export.to_csv(output_dir / 'COMPLETE_ANALYSIS_DATASET.csv', index=False)
dataset_export.to_excel(output_dir / 'COMPLETE_ANALYSIS_DATASET.xlsx', index=False)

print(f"✓ Exported {len(dataset_export)} observations")

# 2. Export correlation matrix
corr_vars = ['ROA', 'AFFECTED_RATIO', 'LOG_ASSETS', 'LEVERAGE', 
             'num_disasters', 'total_facilities', 'exposed_facilities']
corr_vars = [v for v in corr_vars if v in analysis_data.columns]

correlation_matrix = analysis_data[corr_vars].corr()
correlation_matrix.to_csv(output_dir / '04_CORRELATION_MATRIX.csv')
correlation_matrix.to_excel(output_dir / '04_CORRELATION_MATRIX.xlsx')

print("✓ Exported correlation matrix")
print(correlation_matrix)
```

## Final Checklist Before Sending to Professor Yang

- [ ] Run Notebook 5 to generate the dataset
- [ ] Generate correlation matrix
- [ ] Verify all files are present in `statistical_analysis_outputs/`
- [ ] Check that `COMPLETE_ANALYSIS_DATASET.csv` has 2,080 rows
- [ ] Review `README_FOR_PROFESSOR.md` for completeness
- [ ] Package all files in a ZIP file or share the folder

## File Inventory (Complete Package for Professor Yang)

```
statistical_analysis_outputs/
├── 00_README.txt                              ✅ Ready
├── 01_DATASET_DESCRIPTION.txt                 ✅ Ready
├── 02_STATISTICAL_MODEL.txt                   ✅ Ready (KEY DELIVERABLE)
├── 03_DESCRIPTIVE_STATISTICS.csv/.xlsx        ✅ Ready (KEY DELIVERABLE)
├── 03b_EXPOSURE_DISTRIBUTION.csv/.xlsx        ✅ Ready
├── 04_CORRELATION_MATRIX.csv/.xlsx            ⚠️  Need to generate (KEY DELIVERABLE)
├── 05a_REGRESSION_MODEL1_SIMPLE.csv/.xlsx     ✅ Ready (KEY DELIVERABLE)
├── 05b_REGRESSION_MODEL2_CONTROLS.csv/.xlsx   ✅ Ready (KEY DELIVERABLE)
├── 05c_REGRESSION_MODEL3_YEAR_FE.csv/.xlsx    ✅ Ready (KEY DELIVERABLE)
├── 05d_REGRESSION_SUMMARY.csv/.xlsx           ✅ Ready (KEY DELIVERABLE)
├── COMPLETE_ANALYSIS_DATASET.csv/.xlsx        ⚠️  Need to generate (KEY DELIVERABLE)
└── DATA_DICTIONARY.csv                        ⚠️  Need to generate

README_FOR_PROFESSOR.md                        ✅ Ready (Master documentation)
```

## What to Tell Professor Yang

Dear Professor Yang,

I've prepared all the statistical analysis outputs you requested:

1. **Statistical Model** - See `02_STATISTICAL_MODEL.txt`
2. **Descriptive Statistics** - See `03_DESCRIPTIVE_STATISTICS.xlsx`
3. **Regression Results** - See `05a` through `05d` files (all models with complete coefficients)
4. **Complete Dataset** - `COMPLETE_ANALYSIS_DATASET.csv` (2,080 observations)
5. **Correlation Matrix** - `04_CORRELATION_MATRIX.xlsx`

The `README_FOR_PROFESSOR.md` file provides a comprehensive summary of:
- Research question and main findings
- Sample description (2,080 firm-years, 293 companies, 2016-2023)
- Model specifications (3 models with increasing controls)
- Interpretation of the null finding
- Data sources and methodology

Key Finding: Natural disasters do NOT significantly affect ROA in manufacturing firms (p > 0.50 across all models), suggesting resilience due to insurance, diversification, and operational flexibility.

Please let me know if you need any clarifications or additional analyses.

Best regards,
Apoorv Saxena

## Support

If you encounter any issues:
1. Check that all notebooks ran successfully (especially Notebook 5)
2. Verify Google Drive data files are accessible
3. Ensure the `analysis_data` DataFrame exists in Notebook 5's memory
4. Re-run `generate_statistical_outputs.py` if needed to regenerate template files

## Summary

**Already Done:**
- ✅ Model specification document
- ✅ Descriptive statistics (ready to use)
- ✅ Regression tables with all coefficients (ready to use)
- ✅ Comprehensive documentation

**To Do:**
- ⚠️  Generate complete dataset from Notebook 5 (requires data access)
- ⚠️  Generate correlation matrix from Notebook 5 (requires data access)

The `export_dataset_and_correlation.py` script automates both remaining tasks.
