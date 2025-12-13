# SAMPLE SIZE DIAGNOSTIC REPORT
## Response to Professor Yang's Feedback

**Date:** December 13, 2025
**Issue:** Sample size discrepancy (1,839 vs 16,709 in Hsu et al. 2018)

---

## EXECUTIVE SUMMARY

After thorough analysis of the data pipeline, I have identified **four major bottlenecks** causing the sample size gap:

| Stage | Input | Output | Loss | Bottleneck |
|-------|-------|--------|------|------------|
| TRI-CRSP Matching | 24,303 companies | 4,329 high-confidence | 82.2% | Private companies not in CRSP |
| Company-Year Panel | 11,596 obs | 11,596 obs | 0% | - |
| Capital IQ Merge | 11,596 obs | 2,453 obs | 78.8% | **LIMITED FINANCIAL DATA COVERAGE** |
| Regression (with lag) | 2,453 obs | ~1,839 obs | 25% | Lagged variable requires t-1 |

**Primary Cause:** The Capital IQ financial data only covers 2016-2023 and matches only 332 of the 1,016 TRI-matched companies.

---

## DETAILED PIPELINE ANALYSIS

### Stage 1: TRI Data Loading
```
Input: EPA TRI raw files (2009-2023)
Output: 1,141,457 facility-year records
        29,176 unique facilities
        15,834 unique company names
Status: ✓ COMPLETE
```

### Stage 2: TRI-CRSP Company Matching
```
TRI Companies: 24,303
CRSP Companies: 32,675

Match Results:
  - Exact matches: 3,289 (13.5%)
  - High-confidence fuzzy (≥90%): 1,040 (4.3%)
  - Medium-confidence (70-89%): 12,054 (49.6%) ⚠️ NOT USED
  - Unmatched (<70%): 7,920 (32.6%)

TOTAL HIGH-CONFIDENCE: 4,329 (17.8%)

Facility-level match rate: 790,414 / 1,148,673 = 68.8%
```

**Why so many unmatched?**
- Many TRI reporters are **private companies** (not in CRSP)
- Subsidiaries report under parent names that differ from CRSP
- Company name variations (abbreviations, legal suffixes)

### Stage 3: Disaster Exposure Linkage
```
SHELDUS disaster events: 141,486 total
Years with data: 2009-2021 ✓
Years WITHOUT data: 2022-2023 ⚠️

Facility-years exposed to disasters: 360,974 (31.6%)
Company-years with any exposure: 5,593 (48.2%)
```

### Stage 4: Financial Data Merge (THE MAIN BOTTLENECK)
```
Capital IQ Coverage:
  - Company-years loaded: 40,559
  - After CRSP matching: 26,056 (64.2%)
  - Unique companies: 3,755
  - Years: 2016-2023 ONLY ⚠️

After merging with TRI disaster panel:
  - Observations: 2,453 (DOWN FROM 11,596)
  - Companies: 332 (DOWN FROM 1,016)
  - Match rate: 21.2%
```

**Why only 332 companies match?**
1. Capital IQ covers mostly large publicly traded companies
2. Many TRI-matched firms are smaller manufacturers not in Capital IQ
3. Time period mismatch: TRI goes back to 2009, but Capital IQ only has 2016+

### Stage 5: Regression Sample
```
After requiring ROA, controls, and creating lags:
  - Final observations: ~1,839
  - Usable years: 2017-2021 (5 years due to lag + SHELDUS ending)
```

---

## COMPARISON WITH HSU ET AL. (2018)

| Dimension | Hsu et al. (2018) | Current Study | Gap |
|-----------|-------------------|---------------|-----|
| **Time Period** | 1988-2014 (26 years) | 2016-2021 (6 years) | 20 years |
| **Financial Data** | Compustat | Capital IQ | Different coverage |
| **Disaster Data** | SHELDUS | SHELDUS | Same |
| **Observations** | 16,709 | 1,839 | 14,870 |
| **Sample Type** | All industries | TRI filers (manufacturing) | Different |

**Key Differences:**
1. Hsu et al. used **26 years** of data vs. our **6 years**
2. Hsu et al. likely used **Compustat** which has broader coverage
3. Our sample is restricted to **TRI filers** (manufacturing focus)

---

## ROOT CAUSE ANALYSIS

### Issue 1: Limited Time Window
- Capital IQ data only covers 2016-2023
- SHELDUS ends in 2021
- Effective window: **2016-2021 (6 years)**
- With lag requirement: **2017-2021 (5 years)**

### Issue 2: Financial Data Coverage Gap
```
Companies in TRI-CRSP panel: 1,016
Companies in Capital IQ with CRSP match: 3,755
Companies in BOTH: 332 (only 32.7% of TRI-matched)
```

The 684 companies (67.3%) lost are likely:
- Smaller manufacturers not covered by Capital IQ
- Companies with different fiscal year reporting
- Recent IPOs or delistings

### Issue 3: Conservative Matching Threshold
Currently using only **high-confidence matches (≥90%)**:
- 4,329 company matches
- Excludes 12,054 medium-confidence matches (70-89%)

---

## RECOMMENDED SOLUTIONS

### Solution 1: Replace Capital IQ with Compustat (HIGHEST PRIORITY)
```
Expected Impact: 3-5x increase in sample size
Effort: Medium (data acquisition + code modification)

Benefits:
- Compustat covers 1988-present (30+ years)
- Better coverage of manufacturing firms
- Standard in academic finance research
- Hsu et al. (2018) likely used this

Action Items:
1. Obtain Compustat access (WRDS or direct)
2. Download annual fundamentals: gvkey, fyear, at, ni, lt, sale
3. Link via CRSP-Compustat merged database (CCM)
4. Extend analysis to 2009-2021 (13 years)
```

### Solution 2: Include Medium-Confidence Matches
```
Expected Impact: +12,054 potential company matches
Effort: High (requires manual review)

Process:
1. Review medium-confidence matches (70-89% score)
2. Accept/reject each based on:
   - Industry match (SIC codes)
   - Headquarters location
   - Name similarity context
3. Expected acceptance rate: ~50% = +6,000 companies
```

### Solution 3: Expand Disaster Data
```
Expected Impact: +2 years of data (2022-2023)
Effort: Low-Medium

Options:
A. Purchase updated SHELDUS data (if available)
B. Use FEMA disaster declarations as supplement
C. Use NOAA Storm Events Database (free)
```

### Solution 4: Relax TRI-Only Constraint
```
Expected Impact: Potentially 5-10x more firms
Effort: High (major research design change)

Consideration:
- Hsu et al. (2018) may not have used TRI
- Could use COMPUSTAT firms directly
- Match to disasters by headquarters state/county
- Trade-off: Lose facility-level granularity
```

---

## IMPLEMENTATION PRIORITY

| Priority | Solution | Expected Gain | Effort | Recommended |
|----------|----------|---------------|--------|-------------|
| 1 | Use Compustat instead of Capital IQ | +10,000 obs | Medium | ✓ YES |
| 2 | Review medium-confidence matches | +2,000 obs | High | ✓ YES |
| 3 | Extend SHELDUS to 2022-2023 | +500 obs | Low | Optional |
| 4 | Remove TRI constraint | +15,000 obs | High | Discuss |

---

## QUICK FIX: Minimum Viable Solution

If time is constrained, here's the fastest path to a larger sample:

1. **Download Compustat from WRDS** (if access available)
   - Annual fundamentals: 1988-2023
   - Key variables: gvkey, fyear, at, ni, lt, sale, sich

2. **Use CRSP-Compustat Merged (CCM) link table**
   - Links PERMNO to GVKEY
   - Standard in finance research

3. **Merge with existing TRI-CRSP matched data**
   - Use PERMNO as key
   - Extends time series to 2009-2021

4. **Re-run regressions**
   - Expected: 8,000-12,000 observations
   - Matches Hsu et al. (2018) methodology

---

## CODE MODIFICATION NEEDED

```python
# CURRENT APPROACH (Capital IQ - Limited)
financial = pd.read_excel('Company Screening Report.xls')  # 2016-2023 only

# RECOMMENDED APPROACH (Compustat via WRDS)
import wrds
conn = wrds.Connection()
compustat = conn.raw_sql("""
    SELECT gvkey, fyear, at, ni, lt, sale, sich
    FROM comp.funda
    WHERE fyear BETWEEN 1988 AND 2023
    AND datafmt = 'STD'
    AND consol = 'C'
    AND indfmt = 'INDL'
""")

# Link to CRSP via CCM
ccm = conn.raw_sql("""
    SELECT gvkey, lpermno as permno, linkdt, linkenddt
    FROM crsp.ccmxpf_linktable
    WHERE linktype IN ('LU', 'LC')
""")

# Merge with TRI data using PERMNO
```

---

## CONCLUSION

The sample size discrepancy is **primarily due to limited Capital IQ financial data coverage**, not a bug in the matching process. The TRI-CRSP matching is working correctly (68.8% of facility-years matched), but the downstream merge with Capital IQ loses 78% of observations.

**Recommended next step:** Acquire Compustat data and re-run the analysis with the extended time series. This should bring the sample size closer to Hsu et al. (2018)'s 16,709 observations.

---

*Report prepared in response to Professor Yang's feedback on December 13, 2025*
