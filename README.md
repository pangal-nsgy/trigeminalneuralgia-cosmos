# Trigeminal Neuralgia Treatment Patterns Analysis

Analysis of regional variation in trigeminal neuralgia treatment across the United States using Epic Cosmos data.

**Target Journal:** Journal of Neurosurgery (JNS)

---

## Methods

### Data Source

- **Database:** Epic Cosmos
- **Study Period:** November 28, 2022 – November 27, 2025 (3 years)
- **Inclusion Criteria:** Patients with ICD-10 diagnosis code G50.0 (Trigeminal Neuralgia)
- **Geographic Scope:** 50 U.S. states + District of Columbia

### Data Structure

The analysis uses two parallel datasets:

1. **State-Level Data** – Individual state-level counts for detailed geographic analysis
2. **Census Region Data** – Aggregated by U.S. Census Region to mitigate small-cell suppression

### Small-Cell Imputation

Epic Cosmos suppresses exact counts ≤10 for privacy protection, displaying them as "10 or fewer."

**Imputation Strategy:**
- Values marked "10 or fewer" are imputed as **5** (midpoint of 1-10 range)
- This is a conservative approach that preserves statistical power while acknowledging uncertainty
- This decision is documented in all output files and manuscripts

### Geographic Exclusions

| Level | Exclusions | Rationale |
|-------|------------|-----------|
| **State-Level** | Alaska | Sample size <10 creates unreliable percentages for visualization |
| **State-Level** | U.S. Territories, International | Outside scope of U.S. regional comparison |
| **Census-Level** | "Others/Territories" region | Small sample size skews regional statistics |

**Note:** Excluded states are retained in national totals but removed from state-level visualizations.

### Statistical Methods

All statistical analyses use **scipy.stats** (Python) for computational validity and reproducibility.

#### Descriptive Statistics
- **Utilization Rates:** Calculated as (n patients on treatment) / (total patients) × 100%
- **95% Confidence Intervals:** Wilson score interval for proportions (more accurate than Wald interval for extreme proportions)

#### Inferential Statistics

| Test | Purpose | Implementation |
|------|---------|----------------|
| **Chi-Square Test** | Compare categorical distributions across regions | `scipy.stats.chi2_contingency()` |
| **Z-Test for Proportions** | Compare individual state/region rates to national average | `scipy.stats.norm.cdf()` for two-tailed p-value |

#### Multiple Comparisons
- State-level comparisons use individual z-tests against national average
- Significance threshold: α = 0.05 (two-tailed)
- P-values reported to 3 decimal places or as "<0.001"

### Confidence Interval Calculation (Wilson Score)

```python
from scipy import stats
import numpy as np

def proportion_ci(x, n, confidence=0.95):
    """Wilson score interval for binomial proportion."""
    p_hat = x / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denominator
    margin = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n) / denominator
    return (center - margin, center + margin)
```

### Z-Test for Proportion vs Reference

```python
from scipy import stats

def z_test_proportion(x, n, p0):
    """Two-tailed z-test comparing observed proportion to reference."""
    p_hat = x / n
    se = np.sqrt(p0 * (1 - p0) / n)
    z = (p_hat - p0) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value
```

---

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `pandas` | ≥2.0 | Data manipulation |
| `numpy` | ≥1.24 | Numerical operations |
| `scipy` | ≥1.11 | Statistical tests (chi-square, z-test, normal distribution) |
| `matplotlib` | ≥3.7 | Figure generation |
| `seaborn` | ≥0.12 | Heatmaps and statistical visualizations |
| `python-docx` | ≥0.8 | Word document export |
| `openpyxl` | ≥3.1 | Excel file reading |

### Installation

```bash
pip install pandas numpy scipy matplotlib seaborn python-docx openpyxl
```

---

## Project Structure

```
.
├── TN_Data/                              # Raw Excel data from Epic Cosmos
│   ├── TN Medication Data.xlsx           # State-level medication counts
│   ├── TN procedures only.xlsx           # State-level procedure counts
│   ├── TN meds and procedures.xlsx       # State-level cross-tabulation
│   ├── Meds and Census Jan 4 2026.xlsx   # Census-level medication counts
│   ├── Procedures and Census.xlsx        # Census-level procedure counts
│   └── TN meds then procedures by census*.xlsx  # Census-level cross-tabulation
│
├── src/
│   ├── config/
│   │   └── analysis_config.py            # Centralized configuration
│   └── utils/
│       └── data_cleaning.py              # Reusable cleaning functions
│
├── analysis/
│   ├── notebooks/
│   │   ├── 01_data_cleaning_state.ipynb  # State-level data cleaning
│   │   ├── 02_statistical_analysis_state.ipynb  # State-level analysis
│   │   ├── 01_data_cleaning_census.ipynb # Census-level data cleaning
│   │   └── 02_statistical_analysis_census.ipynb # Census-level analysis
│   │
│   └── outputs/
│       ├── data/                         # Cleaned CSV files
│       ├── tables/                       # JNS-formatted tables
│       └── figures/                      # Publication-ready figures
│
├── generate_publication_materials.py     # Generate all tables/figures
├── export_jns_submission.py              # Export to Word document
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

---

## Usage

### 1. Run Data Cleaning Notebooks

Execute in order (run all cells):
```
analysis/notebooks/01_data_cleaning_state.ipynb
analysis/notebooks/01_data_cleaning_census.ipynb
```

### 2. Run Statistical Analysis Notebooks

```
analysis/notebooks/02_statistical_analysis_state.ipynb
analysis/notebooks/02_statistical_analysis_census.ipynb
```

### 3. Generate Publication Materials

```bash
python3 generate_publication_materials.py
python3 export_jns_submission.py
```

Output: `analysis/outputs/TN_Treatment_Analysis_JNS_YYYYMMDD_HHMMSS.docx`

---

## Outputs

### Tables

| Table | Description |
|-------|-------------|
| Table 1 | Study Cohort Characteristics (demographics, regional breakdown) |
| Table 2 | National Treatment Utilization (rates + 95% CIs) |
| Table 3 | Treatment Rates by Census Region |
| Table 4 | Chi-Square Tests for Regional Variation |

### Figures

| Figure | Description |
|--------|-------------|
| Figure 1 | National Medication & Procedure Utilization (bar charts + CIs) |
| Figure 2 | State-Level Carbamazepine/Oxcarbazepine Variation |
| Figure 3 | State-Level MVD Utilization Variation |
| Figure 4 | Regional Treatment Heatmaps (medications + procedures) |
| Figure 5 | Surgical Rates by Medication Group (treatment pathways) |

---

## Key Assumptions & Limitations

1. **Imputation of suppressed values:** "10 or fewer" → 5 may over- or under-estimate true counts
2. **Cross-sectional design:** Cannot infer causation or temporal relationships
3. **Epic Cosmos coverage:** Represents Epic EHR users, not all U.S. healthcare
4. **Treatment combinations:** Patients may have multiple medications/procedures
5. **Alaska excluded from state charts:** Sample size too small for reliable percentage comparison

---

## Authors

Stanford Neurosurgery Research  
January 2026

---

## License

This analysis pipeline is designed for internal research use.
