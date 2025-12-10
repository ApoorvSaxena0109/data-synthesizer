"""
COMPREHENSIVE RESEARCH EXPLORATION
==================================
Analyze the disaster-firm data to identify NEW research directions
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# For statistical analysis
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

print("="*80)
print("COMPREHENSIVE DATA EXPLORATION FOR NEW RESEARCH DIRECTIONS")
print("="*80)

# ============================================================================
# SECTION 1: SIMULATE DATA LOADING (Based on notebook outputs)
# ============================================================================
print("\n" + "="*80)
print("SECTION 1: UNDERSTANDING THE DATA STRUCTURE")
print("="*80)

# Based on notebook analysis, here's what we know about the data:
data_summary = {
    "TRI Facilities": {
        "Total facility-years": 1_141_457,
        "Unique facilities": 29_176,
        "Matched to CRSP": "244,872 (21.4%)",
        "Years": "2009-2023 (missing 2011)",
        "States covered": 56,
        "With FIPS codes": "98.9%"
    },
    "CRSP Companies": {
        "Total records": 38_872,
        "Unique companies": 32_675,
        "With tickers": 9_736
    },
    "SHELDUS Disasters": {
        "Total events": 141_486,
        "Analysis window": 35_283,
        "Counties affected": 2_367,
        "Years complete": "2009-2021",
        "Years missing": "2022-2023"
    },
    "Matched Analysis Sample": {
        "Company-years": 2_453,
        "Unique companies": 332,
        "Years": "2016-2023",
        "Effective window": "2016-2021 (1,838 obs)"
    },
    "Key Finding": {
        "Hsu et al. replication": "NULL RESULT",
        "AFFECTED_RATIO_lag1 → ROA": "Coefficient = 0.003, p = 0.65",
        "Interpretation": "No significant disaster impact on ROA in 2016-2021"
    }
}

print("\n📊 DATA SUMMARY:")
for category, details in data_summary.items():
    print(f"\n{category}:")
    for key, value in details.items():
        print(f"  {key}: {value}")

# ============================================================================
# SECTION 2: UNIQUE FEATURES OF THIS DATA
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: WHAT MAKES THIS DATA UNIQUE")
print("="*80)

unique_features = """
1. FACILITY-LEVEL GRANULARITY (Rare in Finance)
   - Most disaster studies use firm-level exposure
   - We have actual facility locations → precise disaster exposure
   - Can measure WITHIN-FIRM geographic distribution

2. MULTI-FACILITY FIRMS
   - Average 5.8 facilities per matched company
   - Range: 1 to 1,495 facilities (Nucor has 249)
   - Enables study of GEOGRAPHIC DIVERSIFICATION

3. GEOGRAPHIC CONCENTRATION
   - 41.3% of firms operate in single state
   - 58.7% operate in multiple states (up to 40)
   - Natural variation in diversification

4. PANEL STRUCTURE
   - 14 years of data (2009-2023)
   - Allows firm fixed effects (controls unobserved heterogeneity)
   - Can study dynamics and persistence

5. COVID PERIOD INCLUDED
   - 2020-2021 captures COVID disruptions
   - Natural experiment potential
   - Interact disasters with pandemic

6. MANUFACTURING FOCUS
   - TRI covers manufacturing facilities
   - Homogeneous industry → cleaner identification
   - Physical operations → disasters matter more

7. EXPOSURE HETEROGENEITY
   - AFFECTED_RATIO varies 0-100%
   - Can study partial vs. full exposure
   - Threshold effects possible
"""

print(unique_features)

# ============================================================================
# SECTION 3: PATTERNS OBSERVED IN THE DATA
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: KEY PATTERNS FROM NOTEBOOK ANALYSIS")
print("="*80)

patterns = """
PATTERN 1: NULL MAIN EFFECT
- AFFECTED_RATIO_lag1 → ROA: NOT significant
- This CONTRASTS with Hsu et al. (2018) negative effect
- Why? Different time period? Sample composition? Adaptation?

PATTERN 2: DISASTER EXPOSURE IS COMMON
- 64.1% of company-years have some disaster exposure
- Mean AFFECTED_RATIO = 0.33 (33% of facilities affected)
- NOT a rare event → firms may have adapted

PATTERN 3: HETEROGENEOUS EXPOSURE
- Some firms: 100% facilities affected
- Others: 0% (never exposed)
- Wide variation in disaster intensity

PATTERN 4: FIRM SIZE MATTERS (SUGGESTIVE)
- Large firms: Coefficient = 0.012 (p = 0.16)
- Small firms: Coefficient = -0.001 (p = 0.87)
- Hint: Size may moderate disaster impact

PATTERN 5: GEOGRAPHIC DIVERSIFICATION MATTERS (SUGGESTIVE)
- Many facilities: Coefficient = 0.016 (p = 0.05)
- Few facilities: Coefficient = -0.001 (p = 0.87)
- Hint: Diversification may be protective

PATTERN 6: LAGGED EFFECTS ACCUMULATE
- Contemporaneous: 0.005 (p = 0.47)
- 1-year lag: 0.007 (p = 0.24)
- 2-year lag: 0.003 (p = 0.61)
- Cumulative 3-year: 0.015 (not individually significant)

PATTERN 7: NO ANTICIPATION (PLACEBO PASSES)
- Future disasters don't affect current ROA (p = 0.94)
- Supports causal interpretation
"""

print(patterns)

# ============================================================================
# SECTION 4: RESEARCH GAPS AND OPPORTUNITIES
# ============================================================================
print("\n" + "="*80)
print("SECTION 4: RESEARCH GAPS AND OPPORTUNITIES")
print("="*80)

research_gaps = """
GAP 1: GEOGRAPHIC DIVERSIFICATION AS INSURANCE
- Most studies: diversification → performance (general)
- Our angle: diversification → disaster RESILIENCE (specific)
- We can measure: % of facilities affected vs. total facilities
- UNIQUE CONTRIBUTION: First to test "geographic hedge" hypothesis

GAP 2: DISASTER LEARNING AND ADAPTATION
- First disaster vs. repeat disasters
- Do firms learn? Do they relocate? Do they insure?
- Panel structure enables tracking over time

GAP 3: CONCENTRATION VS. DIVERSIFICATION TRADE-OFF
- Geographic concentration → operational efficiency
- But also → disaster vulnerability
- Optimal level of diversification?

GAP 4: COVID AS AMPLIFIER/MITIGATOR
- Do disasters during COVID have different effects?
- Supply chain disruptions already present
- Marginal impact of disasters changes

GAP 5: FACILITY-LEVEL DYNAMICS
- Which facilities close after disasters?
- Do firms relocate production?
- Facility entry/exit patterns

GAP 6: NON-LINEAR EFFECTS
- Threshold effects (disasters only matter above X%)
- Diminishing/increasing marginal effects
- Interaction with firm characteristics

GAP 7: DISASTER TYPE HETEROGENEITY
- Hurricanes vs. floods vs. tornadoes
- Different impact patterns
- Industry vulnerability varies by type
"""

print(research_gaps)

# ============================================================================
# SECTION 5: PROPOSED RESEARCH QUESTIONS
# ============================================================================
print("\n" + "="*80)
print("SECTION 5: PROPOSED RESEARCH QUESTIONS")
print("="*80)

research_questions = """
╔══════════════════════════════════════════════════════════════════════════════╗
║ RESEARCH QUESTION 1: GEOGRAPHIC DIVERSIFICATION AS DISASTER INSURANCE        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Question: Does geographic diversification of facilities protect firms        ║
║           from the negative effects of natural disasters?                    ║
║                                                                              ║
║ Hypothesis: Firms with geographically dispersed facilities experience       ║
║             smaller performance declines when disasters strike.              ║
║                                                                              ║
║ Variables:                                                                   ║
║   - GEOGRAPHIC_HHI = Σ(share_state)² (concentration index)                  ║
║   - NUM_STATES = count of states where firm operates                        ║
║   - AFFECTED_RATIO × DIVERSIFICATION (interaction)                          ║
║                                                                              ║
║ Model:                                                                       ║
║   ROA_it = β₁·AFFECTED_RATIO_lag1 + β₂·GEO_DIVERSIFICATION                  ║
║          + β₃·AFFECTED_RATIO_lag1 × GEO_DIVERSIFICATION                     ║
║          + Controls + Firm_FE + Year_FE + ε                                 ║
║                                                                              ║
║ Expected: β₁ < 0 (disasters hurt), β₃ > 0 (diversification mitigates)      ║
║                                                                              ║
║ Contribution: First facility-level test of "geographic hedge" hypothesis    ║
║ Journals: Management Science, Strategic Management Journal, JFE             ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║ RESEARCH QUESTION 2: DISASTER LEARNING - DO FIRMS ADAPT?                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Question: Do firms that experience disasters become more resilient          ║
║           to subsequent disasters?                                           ║
║                                                                              ║
║ Hypothesis: The negative impact of disasters decreases with experience.     ║
║             "Learning by suffering" creates organizational resilience.       ║
║                                                                              ║
║ Variables:                                                                   ║
║   - CUMULATIVE_DISASTERS = historical disaster count                        ║
║   - FIRST_DISASTER = indicator for first-time exposure                      ║
║   - YEARS_SINCE_FIRST = time since first disaster                           ║
║                                                                              ║
║ Model:                                                                       ║
║   ROA_it = β₁·DISASTER_it + β₂·EXPERIENCE_it                               ║
║          + β₃·DISASTER_it × EXPERIENCE_it                                   ║
║          + Controls + FE + ε                                                ║
║                                                                              ║
║ Expected: β₃ > 0 (experience reduces disaster impact)                       ║
║                                                                              ║
║ Contribution: First study of disaster learning in corporate context         ║
║ Journals: Organization Science, SMJ, Journal of Operations Management      ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║ RESEARCH QUESTION 3: OPERATIONAL CONCENTRATION TRADE-OFF                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Question: Is there an optimal level of geographic concentration that        ║
║           balances operational efficiency against disaster risk?             ║
║                                                                              ║
║ Hypothesis: Moderate concentration maximizes risk-adjusted performance.     ║
║             Too concentrated = disaster vulnerable                           ║
║             Too dispersed = operationally inefficient                        ║
║                                                                              ║
║ Variables:                                                                   ║
║   - CONCENTRATION² (quadratic term)                                         ║
║   - CONCENTRATION × DISASTER_PRONE_REGION                                   ║
║                                                                              ║
║ Model:                                                                       ║
║   ROA_it = β₁·CONCENTRATION + β₂·CONCENTRATION²                            ║
║          + β₃·AFFECTED_RATIO × CONCENTRATION + FE + ε                      ║
║                                                                              ║
║ Expected: Inverted-U relationship (β₁ > 0, β₂ < 0)                         ║
║                                                                              ║
║ Contribution: Optimal diversification framework with disaster risk          ║
║ Journals: Management Science, Operations Research, JOM                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║ RESEARCH QUESTION 4: COVID × DISASTERS - COMPOUNDING CRISES                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Question: Did COVID-19 amplify or mitigate the impact of natural disasters? ║
║                                                                              ║
║ Hypothesis A: COVID amplifies (supply chains already strained)              ║
║ Hypothesis B: COVID mitigates (already operating at reduced capacity)       ║
║                                                                              ║
║ Variables:                                                                   ║
║   - COVID_PERIOD = 1 if year ∈ {2020, 2021}                                ║
║   - AFFECTED_RATIO × COVID_PERIOD                                           ║
║                                                                              ║
║ Model:                                                                       ║
║   ROA_it = β₁·AFFECTED_RATIO + β₂·COVID                                    ║
║          + β₃·AFFECTED_RATIO × COVID + FE + ε                              ║
║                                                                              ║
║ Expected: Empirical question (could go either way)                          ║
║                                                                              ║
║ Contribution: First study of compounding climate + pandemic risks           ║
║ Journals: Nature Climate Change, JFE, Management Science                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║ RESEARCH QUESTION 5: DISASTER TYPES AND INDUSTRY VULNERABILITY              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Question: Do different disaster types have heterogeneous effects across     ║
║           industries, and how do firms in vulnerable industries adapt?       ║
║                                                                              ║
║ Hypothesis: Floods hurt facilities differently than wind events.            ║
║             Chemical plants vulnerable to flooding; warehouses to wind.      ║
║                                                                              ║
║ Variables:                                                                   ║
║   - FLOOD_EXPOSURE, WIND_EXPOSURE, HEAT_EXPOSURE                           ║
║   - INDUSTRY_VULNERABILITY (based on SIC codes)                             ║
║                                                                              ║
║ Contribution: Granular analysis of climate risk by disaster type            ║
║ Journals: Journal of Environmental Economics, JFQA, RFS                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print(research_questions)

# ============================================================================
# SECTION 6: RECOMMENDED BEST RESEARCH DIRECTION
# ============================================================================
print("\n" + "="*80)
print("SECTION 6: RECOMMENDED BEST RESEARCH DIRECTION")
print("="*80)

recommendation = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🏆 RECOMMENDED: RESEARCH QUESTION 1                       ║
║         GEOGRAPHIC DIVERSIFICATION AS NATURAL DISASTER INSURANCE            ║
╚══════════════════════════════════════════════════════════════════════════════╝

WHY THIS IS THE BEST USE OF THIS DATA:
======================================

1. LEVERAGES UNIQUE DATA FEATURE
   - Facility-level data is RARE in finance
   - We can measure WITHIN-FIRM geographic distribution
   - No other dataset allows this precise measurement

2. BUILDS ON (DOESN'T REPLICATE) HSU ET AL. 2018
   - They found: disasters → negative ROA
   - We ask: WHEN do disasters affect ROA?
   - Answer: Depends on firm's geographic footprint

3. EXPLAINS THE NULL RESULT
   - Why no effect in our sample? Maybe firms are diversified
   - If diversified firms dominate → aggregate effect is muted
   - Heterogeneous effects wash out in aggregate

4. HIGH FEASIBILITY
   - All variables can be constructed from existing data
   - No additional data collection needed
   - Clear econometric specification

5. STRONG THEORETICAL FOUNDATION
   - Geographic diversification literature (existing)
   - Corporate risk management (existing)
   - Climate risk (growing)
   - Our contribution: INTERSECTION of these literatures

6. PRACTICAL RELEVANCE
   - Managers: How should we distribute facilities?
   - Investors: How to assess climate risk?
   - Policymakers: Should we encourage geographic spread?

7. TIMELY TOPIC
   - Climate change → more disasters
   - Supply chain disruptions (post-COVID)
   - ESG/climate risk disclosure requirements

JOURNALS LIKELY TO BE INTERESTED:
=================================
- Management Science (operations + strategy)
- Strategic Management Journal (diversification strategy)
- Journal of Financial Economics (corporate risk)
- Review of Financial Studies (climate finance)
- Journal of Operations Management (supply chain)

MAIN HYPOTHESIS:
================
H1: Geographic diversification (measured as facility dispersion across states)
    reduces the negative impact of natural disasters on firm performance.

    Formally: ∂²ROA / ∂DISASTER∂DIVERSIFICATION > 0

ECONOMETRIC MODEL:
==================
ROA_it = β₁·AFFECTED_RATIO_lag1
       + β₂·GEO_DIVERSIFICATION_it
       + β₃·AFFECTED_RATIO_lag1 × GEO_DIVERSIFICATION_it
       + β₄·LOG_ASSETS_it
       + β₅·LEVERAGE_it
       + α_i (firm FE)
       + γ_t (year FE)
       + ε_it

Where:
- GEO_DIVERSIFICATION = 1 - HHI_state (higher = more diversified)
- HHI_state = Σ(facilities_in_state / total_facilities)²

EXPECTED FINDINGS:
==================
- β₁ < 0: Disasters hurt concentrated firms
- β₂ > 0: Diversified firms perform better (efficiency channel unclear)
- β₃ > 0: MAIN RESULT - Diversification mitigates disaster impact

ROBUSTNESS CHECKS:
==================
1. Alternative diversification measures (# states, entropy)
2. IV for diversification (historical disasters → diversification)
3. Placebo: Non-disaster years
4. Heterogeneity by firm size
5. Different disaster types
"""

print(recommendation)

# ============================================================================
# SECTION 7: VARIABLE CONSTRUCTION PLAN
# ============================================================================
print("\n" + "="*80)
print("SECTION 7: VARIABLE CONSTRUCTION FOR RECOMMENDED RESEARCH")
print("="*80)

variable_construction = """
DEPENDENT VARIABLE:
- ROA_it = Net Income / Total Assets (from Capital IQ)

KEY INDEPENDENT VARIABLES:

1. AFFECTED_RATIO_it = exposed_facilities / total_facilities
   Already constructed ✓

2. AFFECTED_RATIO_lag1_it = AFFECTED_RATIO shifted by 1 year within firm
   Already constructed ✓

3. GEO_DIVERSIFICATION_it:
   Step 1: Count facilities per state for each company-year
   Step 2: Calculate state shares: share_s = facilities_s / total_facilities
   Step 3: Calculate HHI: HHI = Σ(share_s)²
   Step 4: DIVERSIFICATION = 1 - HHI (higher = more diversified)

   Interpretation:
   - HHI = 1 → All facilities in one state (concentrated)
   - HHI → 0 → Facilities spread evenly across many states (diversified)
   - DIVERSIFICATION = 1 - HHI → Higher values = more diversified

4. ALTERNATIVE MEASURES:
   - NUM_STATES = count of unique states
   - ENTROPY = -Σ(share_s × log(share_s))
   - GEOGRAPHIC_SPREAD = max distance between facilities

5. INTERACTION TERM:
   - AFFECTED_RATIO_lag1 × GEO_DIVERSIFICATION

CONTROL VARIABLES:
- LOG_ASSETS (firm size)
- LEVERAGE (financial risk)
- ROA_lag1 (persistence)
- Industry indicators (if variation exists)

FIXED EFFECTS:
- Firm FE (α_i): Controls for time-invariant firm characteristics
- Year FE (γ_t): Controls for aggregate time shocks (e.g., recessions)

STANDARD ERRORS:
- Clustered at firm level (accounts for within-firm correlation)
"""

print(variable_construction)

print("\n" + "="*80)
print("EXPLORATION COMPLETE")
print("="*80)
print("\nNext step: Implement preliminary analysis using the facility-level data")
print("="*80)
