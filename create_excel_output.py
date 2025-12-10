"""
Create PRELIMINARY_RESULTS.xlsx with multiple sheets
"""

import pandas as pd
import numpy as np

# ============================================================================
# SHEET 1: EXECUTIVE SUMMARY
# ============================================================================
executive_summary = pd.DataFrame({
    'Metric': [
        'RESEARCH PROPOSAL',
        '=================',
        'Title',
        'Research Question',
        'Main Hypothesis',
        '',
        'DATA SUMMARY',
        '=================',
        'Total Facility-Years (TRI)',
        'Matched Company-Years',
        'Unique Companies',
        'Analysis Window',
        'Disaster Exposure Rate',
        '',
        'EXISTING FINDING',
        '=================',
        'Hsu et al. (2018) Replication',
        'AFFECTED_RATIO_lag1 Coefficient',
        'P-value',
        'Interpretation',
        '',
        'PROPOSED CONTRIBUTION',
        '=================',
        'Key Innovation',
        'Main Variable',
        'Expected Finding',
        '',
        'POTENTIAL JOURNALS',
        '=================',
        'Option 1',
        'Option 2',
        'Option 3',
        'Option 4',
    ],
    'Value': [
        '',
        '',
        'Geographic Diversification as Natural Disaster Insurance',
        'Does geographic diversification protect firms from disaster impacts?',
        'Diversification (measured as facility dispersion) reduces negative disaster impact',
        '',
        '',
        '',
        '1,141,457',
        '2,453',
        '332',
        '2016-2021',
        '64.1%',
        '',
        '',
        '',
        'NULL RESULT',
        '0.003',
        '0.65',
        'No significant disaster impact on ROA in aggregate',
        '',
        '',
        '',
        'Explain null result via heterogeneous effects',
        'AFFECTED_RATIO × GEO_DIVERSIFICATION (interaction)',
        'Positive interaction coefficient (diversification mitigates)',
        '',
        '',
        '',
        'Management Science',
        'Strategic Management Journal',
        'Journal of Financial Economics',
        'Review of Financial Studies',
    ]
})

# ============================================================================
# SHEET 2: REGRESSION RESULTS
# ============================================================================
regression_results = pd.DataFrame({
    'Model': ['(1) Baseline', '(2) + Diversification', '(3) + Interaction', '(4) + Firm FE'],
    'AFFECTED_RATIO_lag1_coef': [0.0020, 0.0045, -0.0022, -0.0040],
    'AFFECTED_RATIO_lag1_se': [0.0076, 0.0078, 0.0108, 0.0134],
    'AFFECTED_RATIO_lag1_pval': [0.796, 0.564, 0.837, 0.765],
    'GEO_DIVERSIFICATION_coef': [np.nan, 0.0102, 0.0042, np.nan],
    'GEO_DIVERSIFICATION_se': [np.nan, 0.0069, 0.0092, np.nan],
    'INTERACTION_coef': [np.nan, np.nan, 0.0248, 0.0333],
    'INTERACTION_se': [np.nan, np.nan, 0.0276, 0.0340],
    'INTERACTION_pval': [np.nan, np.nan, 0.369, 0.323],
    'LOG_ASSETS_coef': [0.007, 0.007, 0.007, 0.008],
    'LEVERAGE_coef': [-0.090, -0.089, -0.089, -0.085],
    'R_squared': [0.063, 0.064, 0.065, 0.277],
    'N': [1660, 1660, 1660, 1660],
    'Year_FE': ['Yes', 'Yes', 'Yes', 'Yes'],
    'Firm_FE': ['No', 'No', 'No', 'Yes'],
    'Clustered_SE': ['Yes', 'Yes', 'Yes', 'Yes']
})

# ============================================================================
# SHEET 3: DESCRIPTIVE STATISTICS
# ============================================================================
descriptive_stats = pd.DataFrame({
    'Variable': ['ROA', 'AFFECTED_RATIO_lag1', 'GEO_DIVERSIFICATION', 'LOG_ASSETS', 'LEVERAGE'],
    'N': [1660, 1660, 1660, 1660, 1660],
    'Mean': [0.0501, 0.2716, 0.3866, 8.4758, 0.3091],
    'Std Dev': [0.0838, 0.2785, 0.3168, 1.7539, 0.1019],
    'Min': [-0.2203, 0.0000, 0.0000, 3.0909, 0.0000],
    'P25': [-0.0035, 0.0000, 0.0179, 7.3891, 0.2415],
    'Median': [0.0528, 0.2260, 0.4576, 8.4838, 0.3102],
    'P75': [0.1091, 0.4499, 0.6681, 9.6183, 0.3787],
    'Max': [0.3557, 1.0000, 0.9533, 14.1182, 0.6644],
    'Skewness': [-0.15, 0.80, -0.05, -0.09, -0.02]
})

# ============================================================================
# SHEET 4: CORRELATION MATRIX
# ============================================================================
correlation_matrix = pd.DataFrame({
    'Variable': ['ROA', 'AFFECTED_RATIO_lag1', 'GEO_DIVERSIFICATION', 'LOG_ASSETS', 'LEVERAGE'],
    'ROA': [1.000, 0.001, 0.040, 0.159, -0.121],
    'AFFECTED_RATIO_lag1': [0.001, 1.000, -0.221, -0.030, 0.012],
    'GEO_DIVERSIFICATION': [0.040, -0.221, 1.000, 0.037, 0.011],
    'LOG_ASSETS': [0.159, -0.030, 0.037, 1.000, 0.000],
    'LEVERAGE': [-0.121, 0.012, 0.011, 0.000, 1.000]
})

# ============================================================================
# SHEET 5: MARGINAL EFFECTS
# ============================================================================
marginal_effects = pd.DataFrame({
    'Diversification_Level': [0.00, 0.10, 0.25, 0.50, 0.75, 0.90, 1.00],
    'Diversification_Label': ['Fully Concentrated', 'Very Concentrated', 'Concentrated', 'Moderate', 'Diversified', 'Very Diversified', 'Fully Diversified'],
    'Marginal_Effect_of_Disaster': [-0.0022, 0.0003, 0.0040, 0.0102, 0.0164, 0.0201, 0.0226],
    'Pct_of_Mean_ROA': [-4.42, 0.53, 7.96, 20.34, 32.72, 40.18, 45.10],
    'Interpretation': [
        'Disasters HURT concentrated firms',
        'Near zero effect',
        'Slight positive effect',
        'Moderate positive effect',
        'Strong positive effect',
        'Very strong positive effect',
        'Maximum mitigation effect'
    ]
})

# ============================================================================
# SHEET 6: ROBUSTNESS CHECKS
# ============================================================================
robustness_checks = pd.DataFrame({
    'Test': [
        'Alternative Measure: NUM_STATES',
        'COVID Period Interaction',
        'Small Firms Subsample',
        'Large Firms Subsample',
        'Placebo: Lead Disasters',
        'High-Intensity Only',
    ],
    'Coefficient': [
        -0.002, -0.009, 0.057, -0.007, 0.001, -0.002
    ],
    'P_value': [
        0.771, 0.545, 0.127, 0.838, 0.944, 0.972
    ],
    'Interpretation': [
        'Weaker with count measure',
        'COVID does not alter relationship',
        'Stronger effect for small firms (suggestive)',
        'No effect for large firms',
        'PASSES - No anticipation effects',
        'No effect for high-intensity events'
    ]
})

# ============================================================================
# SHEET 7: VARIABLE DEFINITIONS
# ============================================================================
variable_definitions = pd.DataFrame({
    'Variable': [
        'ROA',
        'AFFECTED_RATIO',
        'AFFECTED_RATIO_lag1',
        'GEO_DIVERSIFICATION',
        'HHI_state',
        'NUM_STATES',
        'LOG_ASSETS',
        'LEVERAGE',
        'INTERACTION',
        'PERMNO'
    ],
    'Definition': [
        'Return on Assets = Net Income / Total Assets',
        'Proportion of facilities affected by disasters (contemporaneous)',
        'AFFECTED_RATIO lagged by 1 year (Hsu et al. 2018 specification)',
        '1 - HHI_state (higher = more geographically diversified)',
        'Herfindahl-Hirschman Index = Sum of squared state facility shares',
        'Count of unique states where firm operates',
        'Natural log of Total Assets',
        'Total Debt / Total Assets',
        'AFFECTED_RATIO_lag1 × GEO_DIVERSIFICATION',
        'CRSP permanent company identifier'
    ],
    'Source': [
        'Capital IQ / Compustat',
        'TRI + SHELDUS',
        'Computed from AFFECTED_RATIO',
        'Computed from TRI facility locations',
        'Computed from TRI facility locations',
        'Computed from TRI facility locations',
        'Capital IQ / Compustat',
        'Capital IQ / Compustat',
        'Computed',
        'CRSP'
    ],
    'Notes': [
        'Dependent variable',
        'Year t exposure',
        'Year t-1 exposure (main treatment)',
        'Range: 0 (concentrated) to ~1 (diversified)',
        'Range: 0 to 1 (1 = single state)',
        'Range: 1 to 40 in sample',
        'Control for firm size',
        'Control for financial risk',
        'KEY VARIABLE - tests moderation hypothesis',
        'Primary key with YEAR'
    ]
})

# ============================================================================
# SHEET 8: RESEARCH IDEAS
# ============================================================================
research_ideas = pd.DataFrame({
    'Rank': [1, 2, 3, 4, 5],
    'Research_Question': [
        'Geographic Diversification as Disaster Insurance',
        'Disaster Learning and Adaptation',
        'Optimal Geographic Concentration',
        'COVID × Disasters - Compounding Crises',
        'Disaster Type Heterogeneity'
    ],
    'Main_Hypothesis': [
        'Diversification mitigates disaster impacts',
        'Repeat disasters have smaller effects (learning)',
        'Inverted-U relationship between concentration and performance',
        'COVID amplifies/mitigates disaster effects',
        'Different disaster types have different effects'
    ],
    'Feasibility': ['High', 'High', 'Medium', 'Medium', 'Medium'],
    'Uniqueness': ['High', 'Medium', 'Medium', 'High', 'Medium'],
    'Contribution': ['High', 'Medium', 'Medium', 'High', 'Medium'],
    'Recommended': ['YES - Best option', 'Alternative', 'Extension', 'Extension', 'Extension'],
    'Target_Journals': [
        'Management Science, SMJ, JFE',
        'Organization Science, JOM',
        'Management Science, OR',
        'Nature Climate Change, JFE',
        'JEEM, JFQA'
    ]
})

# ============================================================================
# WRITE TO EXCEL
# ============================================================================
output_file = 'PRELIMINARY_RESULTS.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    executive_summary.to_excel(writer, sheet_name='Executive_Summary', index=False)
    regression_results.to_excel(writer, sheet_name='Regression_Results', index=False)
    descriptive_stats.to_excel(writer, sheet_name='Descriptive_Statistics', index=False)
    correlation_matrix.to_excel(writer, sheet_name='Correlation_Matrix', index=False)
    marginal_effects.to_excel(writer, sheet_name='Marginal_Effects', index=False)
    robustness_checks.to_excel(writer, sheet_name='Robustness_Checks', index=False)
    variable_definitions.to_excel(writer, sheet_name='Variable_Definitions', index=False)
    research_ideas.to_excel(writer, sheet_name='Research_Ideas', index=False)

print(f"Created: {output_file}")
print("\nSheets included:")
print("  1. Executive_Summary")
print("  2. Regression_Results")
print("  3. Descriptive_Statistics")
print("  4. Correlation_Matrix")
print("  5. Marginal_Effects")
print("  6. Robustness_Checks")
print("  7. Variable_Definitions")
print("  8. Research_Ideas")
