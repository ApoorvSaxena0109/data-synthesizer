# REFINED RESEARCH PROPOSAL
## Production Flexibility and Corporate Resilience: How Multi-Facility Networks Absorb Disaster Shocks

---

## THE PUZZLE THAT MOTIVATES THIS RESEARCH

**Observation 1:** Natural disasters cause massive economic damage ($150B+ annually in the US)

**Observation 2:** Firm-level studies find WEAK or NULL effects of disasters on profitability

**The puzzle:** How can disasters cause enormous aggregate damage but not hurt individual firms?

**Our answer:** Firms with multiple facilities ABSORB shocks through production reallocation. The null aggregate effect masks heterogeneous responses.

---

## WHY PREVIOUS STUDIES MISS THE STORY

### The Hsu et al. (2018) Approach

```
ROA_it = β·DISASTER_it + Controls + FE + ε
```

**Problem 1:** Treats all firms the same
- A firm with 1 facility vs. 100 facilities respond differently
- The average β pools these together

**Problem 2:** Uses firm-level disaster exposure
- Misses within-firm variation
- Can't see if some facilities are hit while others compensate

**Problem 3:** Looks only at financial outcomes
- ROA is an EQUILIBRIUM outcome
- Misses the PROCESS by which firms adjust

### What We Do Differently

We leverage facility-level data to:
1. Observe WHICH facilities are affected
2. Test if OTHER facilities respond
3. Measure the MECHANISM (production reallocation)
4. Show WHEN firms are protected vs. vulnerable

---

## THEORETICAL FRAMEWORK

### The Real Options View of Multi-Facility Networks

A firm with N facilities holds a portfolio of **real options**:
- Option to shift production across facilities
- Option to temporarily shut down affected facilities
- Option to source from different locations

The **value** of these options depends on:
1. **Correlation of disaster risk** across facilities
2. **Spare capacity** at unaffected facilities
3. **Substitutability** of production across sites
4. **Adjustment costs** (logistics, setup)

### Model Setup

Firm i has J facilities in locations {1, ..., J}
- Demand: D
- Capacity at facility j: K_j
- Unit cost at j: c_j
- Disaster hits location j: K_j → 0

**Without reallocation:**
```
Lost profit = (P - c_j) × min(D, K_j)
```

**With reallocation to facility k:**
```
Lost profit = (c_k - c_j + transport) × min(D, K_k)
```

**Prediction 1:** Multi-facility firms lose LESS when disasters strike
**Prediction 2:** The benefit of multiple facilities is LARGER when:
- Other facilities have slack capacity
- Facilities are interchangeable (same products)
- Facilities are not too far apart (low transport cost)

---

## EMPIRICAL STRATEGY

### Stage 1: Establish That Disasters Affect Facilities

**Question:** Do disasters actually disrupt facility operations?

**Approach:** Use TRI emissions as a proxy for production

```
log(Emissions_ijt) = β₁·DISASTER_jt + α_ij + γ_t + ε_ijt

Where:
- Emissions_ijt = TRI reported emissions at facility i in county j at time t
- DISASTER_jt = indicator for disaster in county j at time t
- α_ij = facility fixed effect
- γ_t = year fixed effect
```

**Expected:** β₁ < 0 (disasters reduce facility output)

### Stage 2: Test for Production Reallocation

**Question:** When one facility is hit, do sister facilities increase output?

**Approach:** Within-firm variation

```
log(Emissions_ijt) = β₁·OWN_DISASTER_ijt
                   + β₂·SISTER_DISASTER_it
                   + β₃·SISTER_DISASTER_it × SLACK_ijt
                   + α_ij + γ_it + ε_ijt

Where:
- SISTER_DISASTER_it = any OTHER facility of firm i hit by disaster
- SLACK_ijt = measure of spare capacity at facility j
- γ_it = firm×year fixed effect (absorbs firm-level shocks)
```

**Expected:**
- β₂ > 0 (facilities increase output when sisters are hit)
- β₃ > 0 (effect stronger when facility has slack)

### Stage 3: Link to Firm Financial Performance

**Question:** Does production reallocation explain why diversified firms are unaffected?

**Approach:** Two-stage analysis

First, compute **REALLOCATION_CAPACITY**:
```
REALLOCATION_CAPACITY_it = Σ_j (SLACK_ijt × DISTANCE_ji^{-1}) for j ≠ affected
```
This measures the firm's ability to shift production.

Then estimate:
```
ROA_it = β₁·AFFECTED_RATIO_it
       + β₂·REALLOCATION_CAPACITY_it
       + β₃·AFFECTED_RATIO_it × REALLOCATION_CAPACITY_it
       + Controls + FE + ε
```

**Expected:** β₃ > 0 (reallocation capacity mitigates disaster impact)

### Stage 4: Robustness and Placebo Tests

1. **Placebo: Lead disasters**
   - Future disasters should not affect current operations

2. **Placebo: Distant disasters**
   - Disasters in unrelated counties should not affect facilities

3. **Heterogeneity by product type**
   - Standardized products → easier reallocation → larger mitigation

4. **Instrument for diversification**
   - Use historical disasters in HQ region as instrument
   - Firms exposed to disasters in past → more likely to diversify

---

## DATA CONSTRUCTION

### Variable Definitions

| Variable | Definition | Source |
|----------|------------|--------|
| `EMISSIONS_ijt` | Total TRI releases (lbs) at facility i in county j | TRI Form R |
| `OWN_DISASTER_ijt` | Indicator: disaster in facility's county | SHELDUS |
| `SISTER_DISASTER_it` | Count of sister facilities affected | TRI + SHELDUS |
| `SLACK_ijt` | (Historical max - current) / historical max emissions | Computed |
| `REALLOCATION_CAPACITY_it` | Σ (slack × inverse distance) for unaffected facilities | Computed |
| `GEO_DIVERSIFICATION_it` | 1 - HHI of state facility shares | Computed |
| `NUM_FACILITIES_it` | Count of active facilities | TRI |

### Sample Construction

1. Start with all TRI facilities 2009-2021
2. Match to CRSP for public company identifiers
3. Merge with SHELDUS for disaster exposure
4. Aggregate to facility-year for operations analysis
5. Aggregate to firm-year for financial analysis

Expected sample:
- Facility-years: ~250,000 (matched to public firms)
- Firm-years: ~10,000
- Regression sample (with lags): ~8,000

---

## EXPECTED RESULTS AND INTERPRETATION

### Main Finding Preview

Based on patterns in the existing analysis:

| Specification | DISASTER Effect | INTERACTION Effect | Interpretation |
|--------------|-----------------|-------------------|----------------|
| Pooled | ≈ 0 (null) | N/A | Naive estimate shows no effect |
| + Diversification | Negative | Positive | Concentrated firms hurt; diversified protected |
| + Mechanism | Negative | Positive | Reallocation capacity explains protection |

### Economic Magnitude (Illustrative)

For a firm with average disaster exposure (33% of facilities):
- **Concentrated firm** (1 state): ROA declines 1.5 percentage points
- **Diversified firm** (5+ states): ROA declines 0.2 percentage points
- **Difference:** 1.3 percentage points = 26% of mean ROA

### Why the Aggregate Effect is Null

The sample is dominated by:
- Large firms (by TRI coverage)
- Multi-facility firms (average 5.8 facilities)
- These firms CAN reallocate

If we had small, single-facility firms, we would see negative effects.
The null aggregate masks the heterogeneity.

---

## CONTRIBUTION TO LITERATURE

### 1. Climate Finance / Disaster Economics
- Most studies: aggregate or industry-level effects
- We show: firm-level null masks within-firm adjustment
- Contribution: Explains why firm-level studies find weak effects

### 2. Corporate Diversification
- Traditional view: diversification destroys value (conglomerate discount)
- We show: geographic diversification provides disaster INSURANCE
- Contribution: Identifies a VALUE of diversification

### 3. Operations / Supply Chain
- Growing interest in resilience post-COVID
- We provide: micro-evidence of production reallocation
- Contribution: Shows how firms absorb supply shocks

### 4. Real Options
- Theory: multiple facilities = portfolio of options
- We provide: empirical test of option exercise
- Contribution: Real options in practice

---

## ADDRESSING POTENTIAL CONCERNS

### Concern 1: Endogeneity of Diversification

**Critique:** Diversified firms may be better managed

**Response 1:** Firm fixed effects absorb time-invariant differences

**Response 2:** We use WITHIN-firm variation
- Same firm, different disasters
- Firm's diversification is fixed; disaster exposure varies

**Response 3:** Placebo test
- If it's just "good firms," they should perform well even without disasters
- We interact with disaster exposure

**Response 4:** Mechanism test
- If it's just management quality, why does REALLOCATION CAPACITY matter?
- We show the specific channel through which diversification helps

### Concern 2: Emissions ≠ Production

**Critique:** TRI emissions may not track production

**Response 1:** We use CHANGES not levels
- Facility FE absorbs level differences
- Within-facility variation captures shocks

**Response 2:** Robustness with different emission types
- Air emissions, water discharges, waste
- If all move together, likely production-driven

**Response 3:** Validate with subset
- For firms with segment data, check correlation with segment revenue

### Concern 3: External Validity

**Critique:** TRI covers only large manufacturers

**Response:**
- This is the RIGHT sample for studying production reallocation
- Manufacturing firms have physical operations; disasters matter more
- Acknowledge limitation; suggest future work on services

### Concern 4: Disaster Anticipation

**Critique:** Firms may prepare for expected disasters

**Response 1:** Use unexpected component
- Regress disaster on historical patterns
- Residual = surprise

**Response 2:** Rapid-onset disasters
- Tornadoes, earthquakes cannot be anticipated
- Robustness with these types only

---

## TIMELINE AND DELIVERABLES

### Phase 1: Data Construction (2 weeks)
- Calculate facility-level emissions by year
- Compute SLACK and REALLOCATION_CAPACITY
- Merge all datasets at facility and firm level

### Phase 2: Facility-Level Analysis (2 weeks)
- Estimate disaster effect on facility operations
- Test production reallocation hypothesis
- Document within-firm adjustment

### Phase 3: Firm-Level Analysis (2 weeks)
- Link facility patterns to firm ROA
- Estimate interaction effects
- Show mechanism explains heterogeneity

### Phase 4: Robustness and Writing (4 weeks)
- All robustness checks
- Write paper
- Prepare for submission

**Total:** 10 weeks to complete draft

---

## TARGET JOURNALS

### First Choice: Management Science
- Operations + Finance intersection
- Values micro-evidence of firm behavior
- Recent interest in climate/resilience

### Second Choice: Journal of Financial Economics
- Climate finance is growing area
- Corporate risk management angle
- Need to emphasize asset pricing implications

### Third Choice: Strategic Management Journal
- Geographic strategy angle
- Diversification literature
- Competitive implications

---

## CONCLUDING THOUGHTS

This research matters because:

1. **Climate change** is increasing disaster frequency
2. **Supply chain disruptions** (COVID) have heightened attention to resilience
3. **Policy makers** need to understand how firms adapt
4. **Investors** need to assess climate risk exposure

Our data allows us to look INSIDE firms and see HOW they absorb shocks. This is unique and valuable.

The null result in the Hsu et al. replication is not a dead end—it's a STARTING POINT. The absence of an average effect is itself a finding that demands explanation. Our explanation: **heterogeneous resilience driven by production flexibility**.

---

*"In research, a null result is often more interesting than a significant one. It forces you to ask: WHY? The answer to why may be more valuable than the effect itself."*
