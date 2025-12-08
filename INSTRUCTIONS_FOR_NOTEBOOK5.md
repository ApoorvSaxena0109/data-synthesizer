# Instructions: Adding Output Generation to Your Notebook 5

## Overview
You have **6 notebooks total** (not creating a new one):
1. Data_Preparation_FIPS.ipynb
2. Automated_Matching_FIPS.ipynb  
3. 03_manual_review_and_analysis.ipynb
4. 04_disaster_exposure_analysis.ipynb
5. **05_CLEAN_affected_ratio_baseline_regression.ipynb** ← Add cell here
6. 06_ROBUSTNESS_CHECKS_CLEAN.ipynb

## What to Do

**Add ONE new code cell at the END of Notebook 5** (05_CLEAN_affected_ratio_baseline_regression.ipynb)

Copy the code from `COLAB_INTEGRATION_CELL.py` and paste it as a new cell in your notebook.

## Why Notebook 5?

Notebook 5 is where you:
- Create the `analysis_data` DataFrame (2,080 observations)
- Run the 3 regression models
- Generate baseline results

After running all cells in Notebook 5, the new cell will:
1. Export `COMPLETE_ANALYSIS_DATASET.csv` (2,080 rows) ✓
2. Generate `CORRELATION_MATRIX.csv` ✓
3. Create `EMAIL_FOR_PROFESSOR.txt` with email content ✓
4. Save everything to your Google Drive

## Step-by-Step

### Step 1: Open Notebook 5 in Google Colab
```
05_CLEAN_affected_ratio_baseline_regression.ipynb
```

### Step 2: Run all existing cells
Make sure your analysis runs successfully and creates `analysis_data`

### Step 3: Add new cell at the end
1. Click "+ Code" at the bottom of the notebook
2. Open `COLAB_INTEGRATION_CELL.py` 
3. Copy ALL the code
4. Paste into the new cell

### Step 4: Run the new cell
It will:
- Export your complete dataset
- Generate correlation matrix  
- Create email content for Professor Yang
- Save everything to Google Drive

### Step 5: Find your files
Look in: `/content/drive/MyDrive/Paper1_Dataset/statistical_analysis_outputs/`

Files created:
- `COMPLETE_ANALYSIS_DATASET.csv` (2,080 rows)
- `COMPLETE_ANALYSIS_DATASET.xlsx`
- `CORRELATION_MATRIX.csv`
- `CORRELATION_MATRIX.xlsx`
- `DATA_DICTIONARY.csv`
- `SUMMARY_BY_EXPOSURE_GROUP.csv`
- `EMAIL_FOR_PROFESSOR.txt` ← **Copy this for your email**

### Step 6: Send to Professor Yang
1. Open `EMAIL_FOR_PROFESSOR.txt`
2. Copy the content
3. Send email with attachments from the output folder

## No New Notebook Needed

You do **NOT** need to create a new 7th notebook. Just add one cell to your existing Notebook 5.

## Manual Alternative

If you prefer to do it manually instead of using the cell:

### Export Dataset Manually:
```python
# In Notebook 5, after all cells run:
dataset_export = analysis_data[['PERMNO', 'YEAR', 'TICKER', 'total_facilities', 
                                 'num_disasters', 'exposed_facilities', 'AFFECTED_RATIO',
                                 'DISASTER', 'ROA', 'TOTAL_ASSETS', 'NET_INCOME', 
                                 'TOTAL_DEBT', 'TOTAL_REVENUE', 'LOG_ASSETS', 
                                 'LEVERAGE']].copy()

dataset_export.to_csv('/content/drive/MyDrive/Paper1_Dataset/COMPLETE_ANALYSIS_DATASET.csv', index=False)
```

### Generate Correlation Matrix Manually:
```python
# In Notebook 5:
corr_vars = ['ROA', 'AFFECTED_RATIO', 'LOG_ASSETS', 'LEVERAGE', 
             'num_disasters', 'total_facilities', 'exposed_facilities']
correlation_matrix = analysis_data[corr_vars].corr()
correlation_matrix.to_csv('/content/drive/MyDrive/Paper1_Dataset/CORRELATION_MATRIX.csv')
```

## Summary

- **6 notebooks total** (you already have them)
- **Add 1 cell to Notebook 5** (not creating new notebook)
- **Run the cell** to generate all outputs
- **Email content will be generated** for you to copy

That's it!
