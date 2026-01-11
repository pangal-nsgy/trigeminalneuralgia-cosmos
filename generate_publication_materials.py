"""
Generate Publication-Ready Tables and Figures
Trigeminal Neuralgia Treatment Patterns Analysis
For Journal of Neurosurgery (JNS) Submission
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'analysis' / 'outputs' / 'data'
TABLES_DIR = PROJECT_ROOT / 'analysis' / 'outputs' / 'tables'
FIGURES_DIR = PROJECT_ROOT / 'analysis' / 'outputs' / 'figures'
OUTPUT_DIR = PROJECT_ROOT / 'analysis' / 'outputs'

# Plot settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

# States to exclude from state-level charts (small n creates unreliable percentages)
STATES_TO_EXCLUDE = ['Alaska']

# US State Populations (2024 Census Bureau Estimates)
US_STATE_POPULATIONS = {
    'Alabama': 5108468, 'Alaska': 733406, 'Arizona': 7431344, 'Arkansas': 3067732,
    'California': 38965193, 'Colorado': 5877610, 'Connecticut': 3617176, 'Delaware': 1031890,
    'District of Columbia': 678972, 'Florida': 23372215, 'Georgia': 11029227, 'Hawaii': 1435138,
    'Idaho': 1964726, 'Illinois': 12516863, 'Indiana': 6862199, 'Iowa': 3207004,
    'Kansas': 2940546, 'Kentucky': 4526154, 'Louisiana': 4573749, 'Maine': 1395722,
    'Maryland': 6180253, 'Massachusetts': 7001399, 'Michigan': 10037261, 'Minnesota': 5737915,
    'Mississippi': 2939690, 'Missouri': 6196156, 'Montana': 1132812, 'Nebraska': 1978379,
    'Nevada': 3194176, 'New Hampshire': 1402054, 'New Jersey': 9290841, 'New Mexico': 2114371,
    'New York': 19571216, 'North Carolina': 10835491, 'North Dakota': 783926, 'Ohio': 11785935,
    'Oklahoma': 4053824, 'Oregon': 4233358, 'Pennsylvania': 12961683, 'Rhode Island': 1095962,
    'South Carolina': 5373555, 'South Dakota': 919318, 'Tennessee': 7126489, 'Texas': 30503301,
    'Utah': 3417734, 'Vermont': 647464, 'Virginia': 8683619, 'Washington': 7812880,
    'West Virginia': 1770071, 'Wisconsin': 5910955, 'Wyoming': 584057,
}

# State abbreviations for plotly choropleth
STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def proportion_ci(x, n, confidence=0.95):
    """Wilson score interval for proportion."""
    if n == 0:
        return 0, 0
    p_hat = x / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denominator
    margin = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n) / denominator
    return max(0, center - margin) * 100, min(1, center + margin) * 100

def format_pvalue(p):
    """Format p-value: 3 decimals or <0.001"""
    if p < 0.001:
        return "<0.001"
    else:
        return f"{p:.3f}"

def z_test_proportion(x, n, p0):
    """Z-test for comparing observed proportion to reference proportion."""
    p_hat = x / n
    se = np.sqrt(p0 * (1 - p0) / n)
    if se == 0:
        return 0, 1.0
    z = (p_hat - p0) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def create_table1(df_meds):
    """Table 1: Study Cohort Characteristics"""
    print("Creating Table 1: Study Cohort Characteristics...")
    
    total = df_meds['total'].sum()
    
    # By census region
    region_data = df_meds.groupby('census_region')['total'].sum().reset_index()
    region_data['pct'] = (region_data['total'] / total * 100).round(1)
    region_data = region_data.sort_values('total', ascending=False)
    
    rows = []
    rows.append({'Characteristic': 'Total TN Patients', 'N': f"{total:,}", 'Percentage': '100.0%'})
    rows.append({'Characteristic': '', 'N': '', 'Percentage': ''})
    rows.append({'Characteristic': 'Census Region', 'N': '', 'Percentage': ''})
    
    for _, row in region_data.iterrows():
        rows.append({
            'Characteristic': f"  {row['census_region']}",
            'N': f"{row['total']:,.0f}",
            'Percentage': f"{row['pct']}%"
        })
    
    rows.append({'Characteristic': '', 'N': '', 'Percentage': ''})
    rows.append({'Characteristic': 'Study Period', 'N': 'Nov 28, 2022 - Nov 27, 2025', 'Percentage': ''})
    rows.append({'Characteristic': 'Data Source', 'N': 'Epic Cosmos', 'Percentage': ''})
    rows.append({'Characteristic': 'ICD-10 Code', 'N': 'G50.0 (Trigeminal Neuralgia)', 'Percentage': ''})
    
    df = pd.DataFrame(rows)
    df.to_csv(TABLES_DIR / 'jns_table1_cohort_characteristics.csv', index=False)
    return df

def create_table_per_capita(df_meds):
    """Create per capita TN diagnosis rates by state."""
    print("Creating Per Capita Rates Table...")
    
    df = df_meds.copy()
    df['population'] = df['state'].map(US_STATE_POPULATIONS)
    df['per_100k'] = df['total'] / df['population'] * 100000
    df['state_abbrev'] = df['state'].map(STATE_ABBREV)
    
    # Sort by per capita rate
    df_sorted = df[['state', 'state_abbrev', 'total', 'population', 'per_100k', 'census_region']].sort_values('per_100k', ascending=False)
    
    # Format for display
    df_display = df_sorted.copy()
    df_display['population'] = df_display['population'].apply(lambda x: f"{x:,}")
    df_display['total'] = df_display['total'].apply(lambda x: f"{x:,}")
    df_display['per_100k'] = df_display['per_100k'].apply(lambda x: f"{x:.1f}")
    df_display.columns = ['State', 'Abbrev', 'TN Patients', 'Population', 'Per 100,000', 'Census Region']
    
    df_display.to_csv(TABLES_DIR / 'jns_table_per_capita_rates.csv', index=False)
    
    # Also save numeric version for mapping
    df_sorted.to_csv(DATA_DIR / 'state_per_capita_rates.csv', index=False)
    
    return df_sorted

def create_table2(df_meds, df_procs):
    """Table 2: National Treatment Utilization"""
    print("Creating Table 2: National Treatment Utilization...")
    
    total = df_meds['total'].sum()
    
    med_cols = ['carbamazepine_oxcarbazepine', 'gabapentin', 'pregabalin', 
                'baclofen', 'lamotrigine', 'onabotulinumtoxina']
    proc_cols = ['mvd', 'srs', 'rhizotomy', 'glycerol_rhizotomy', 'botox']
    
    med_names = {
        'carbamazepine_oxcarbazepine': 'Carbamazepine/Oxcarbazepine',
        'gabapentin': 'Gabapentin',
        'pregabalin': 'Pregabalin',
        'baclofen': 'Baclofen',
        'lamotrigine': 'Lamotrigine',
        'onabotulinumtoxina': 'OnabotulinumtoxinA'
    }
    
    proc_names = {
        'mvd': 'Microvascular Decompression (MVD)',
        'srs': 'Stereotactic Radiosurgery (SRS)',
        'rhizotomy': 'Percutaneous Rhizotomy',
        'glycerol_rhizotomy': 'Glycerol Rhizotomy',
        'botox': 'Botox Injection'
    }
    
    rows = []
    rows.append({'Treatment': 'MEDICATIONS', 'N': '', 'Rate (%)': '', '95% CI': ''})
    
    for col in med_cols:
        if col in df_meds.columns:
            n = df_meds[col].sum()
            rate = n / total * 100
            ci_low, ci_high = proportion_ci(n, total)
            rows.append({
                'Treatment': f"  {med_names.get(col, col)}",
                'N': f"{n:,.0f}",
                'Rate (%)': f"{rate:.1f}",
                '95% CI': f"({ci_low:.1f}-{ci_high:.1f})"
            })
    
    rows.append({'Treatment': '', 'N': '', 'Rate (%)': '', '95% CI': ''})
    rows.append({'Treatment': 'PROCEDURES', 'N': '', 'Rate (%)': '', '95% CI': ''})
    
    for col in proc_cols:
        if col in df_procs.columns:
            n = df_procs[col].sum()
            rate = n / total * 100
            ci_low, ci_high = proportion_ci(n, total)
            rows.append({
                'Treatment': f"  {proc_names.get(col, col)}",
                'N': f"{n:,.0f}",
                'Rate (%)': f"{rate:.2f}",
                '95% CI': f"({ci_low:.2f}-{ci_high:.2f})"
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(TABLES_DIR / 'jns_table2_national_utilization.csv', index=False)
    return df

def create_table3(df_meds, df_procs):
    """Table 3: Treatment Rates by Census Region"""
    print("Creating Table 3: Treatment Rates by Census Region...")
    
    med_cols = ['carbamazepine_oxcarbazepine', 'gabapentin', 'pregabalin', 'baclofen']
    proc_cols = ['mvd', 'srs', 'rhizotomy']
    
    # Aggregate by region
    region_meds = df_meds.groupby('census_region').agg({
        **{col: 'sum' for col in med_cols if col in df_meds.columns},
        'total': 'sum'
    }).reset_index()
    
    region_procs = df_procs.groupby('census_region').agg({
        **{col: 'sum' for col in proc_cols if col in df_procs.columns},
        'total': 'sum'
    }).reset_index()
    
    rows = []
    for _, mrow in region_meds.iterrows():
        region = mrow['census_region']
        prow = region_procs[region_procs['census_region'] == region].iloc[0]
        
        entry = {
            'Census Region': region,
            'N Patients': f"{mrow['total']:,.0f}"
        }
        
        for col in med_cols:
            if col in df_meds.columns:
                rate = mrow[col] / mrow['total'] * 100
                short_name = col.replace('carbamazepine_oxcarbazepine', 'Carb/Oxcarb').replace('gabapentin', 'Gabapentin').replace('pregabalin', 'Pregabalin').replace('baclofen', 'Baclofen')
                entry[f'{short_name} (%)'] = f"{rate:.1f}"
        
        for col in proc_cols:
            if col in df_procs.columns:
                rate = prow[col] / prow['total'] * 100
                short_name = col.upper()
                entry[f'{short_name} (%)'] = f"{rate:.2f}"
        
        rows.append(entry)
    
    df = pd.DataFrame(rows)
    df = df.sort_values('N Patients', key=lambda x: x.str.replace(',', '').astype(int), ascending=False)
    df.to_csv(TABLES_DIR / 'jns_table3_regional_rates.csv', index=False)
    return df

def create_table4(df_meds, df_procs):
    """Table 4: Statistical Tests for Regional Variation"""
    print("Creating Table 4: Statistical Tests...")
    
    med_cols = ['carbamazepine_oxcarbazepine', 'gabapentin', 'pregabalin', 'baclofen', 'lamotrigine']
    proc_cols = ['mvd', 'srs', 'rhizotomy', 'botox']
    
    # Medication chi-square
    region_meds = df_meds.groupby('census_region').agg({
        **{col: 'sum' for col in med_cols if col in df_meds.columns}
    })
    chi2_med, p_med, dof_med, _ = stats.chi2_contingency(region_meds)
    
    # Procedure chi-square
    region_procs = df_procs.groupby('census_region').agg({
        **{col: 'sum' for col in proc_cols if col in df_procs.columns}
    })
    chi2_proc, p_proc, dof_proc, _ = stats.chi2_contingency(region_procs)
    
    rows = [
        {
            'Test': 'Medication Preferences by Region',
            'Chi-Square': f"{chi2_med:.1f}",
            'df': dof_med,
            'P-value': format_pvalue(p_med),
            'Result': 'Significant' if p_med < 0.05 else 'Not Significant'
        },
        {
            'Test': 'Surgical Preferences by Region',
            'Chi-Square': f"{chi2_proc:.1f}",
            'df': dof_proc,
            'P-value': format_pvalue(p_proc),
            'Result': 'Significant' if p_proc < 0.05 else 'Not Significant'
        }
    ]
    
    df = pd.DataFrame(rows)
    df.to_csv(TABLES_DIR / 'jns_table4_chisquare_tests.csv', index=False)
    return df

def create_figure1(df_meds, df_procs):
    """Figure 1: National Treatment Utilization Rates"""
    print("Creating Figure 1: National Utilization Rates...")
    
    total = df_meds['total'].sum()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Medications
    med_cols = ['gabapentin', 'carbamazepine_oxcarbazepine', 'pregabalin', 'baclofen', 'lamotrigine', 'onabotulinumtoxina']
    med_names = ['Gabapentin', 'Carbamazepine/\nOxcarbazepine', 'Pregabalin', 'Baclofen', 'Lamotrigine', 'OnabotulinumtoxinA']
    
    med_rates = []
    med_cis = []
    for col in med_cols:
        if col in df_meds.columns:
            n = df_meds[col].sum()
            rate = n / total * 100
            ci_low, ci_high = proportion_ci(n, total)
            med_rates.append(rate)
            med_cis.append((rate - ci_low, ci_high - rate))
    
    ax1 = axes[0]
    colors_med = plt.cm.Blues(np.linspace(0.4, 0.8, len(med_rates)))
    bars1 = ax1.barh(range(len(med_rates)), med_rates, color=colors_med, edgecolor='black', linewidth=0.5)
    ax1.errorbar(med_rates, range(len(med_rates)), xerr=np.array(med_cis).T, fmt='none', color='black', capsize=3)
    ax1.set_yticks(range(len(med_rates)))
    ax1.set_yticklabels(med_names)
    ax1.set_xlabel('Patients (%)', fontsize=11)
    ax1.set_title('A. Medication Utilization', fontsize=12, fontweight='bold')
    ax1.set_xlim(0, 60)
    
    # Procedures
    proc_cols = ['mvd', 'srs', 'rhizotomy', 'glycerol_rhizotomy', 'botox']
    proc_names = ['MVD', 'SRS', 'Percutaneous\nRhizotomy', 'Glycerol\nRhizotomy', 'Botox']
    
    proc_rates = []
    proc_cis = []
    for col in proc_cols:
        if col in df_procs.columns:
            n = df_procs[col].sum()
            rate = n / total * 100
            ci_low, ci_high = proportion_ci(n, total)
            proc_rates.append(rate)
            proc_cis.append((rate - ci_low, ci_high - rate))
    
    ax2 = axes[1]
    colors_proc = plt.cm.Oranges(np.linspace(0.4, 0.8, len(proc_rates)))
    bars2 = ax2.barh(range(len(proc_rates)), proc_rates, color=colors_proc, edgecolor='black', linewidth=0.5)
    ax2.errorbar(proc_rates, range(len(proc_rates)), xerr=np.array(proc_cis).T, fmt='none', color='black', capsize=3)
    ax2.set_yticks(range(len(proc_rates)))
    ax2.set_yticklabels(proc_names)
    ax2.set_xlabel('Patients (%)', fontsize=11)
    ax2.set_title('B. Surgical Procedure Utilization', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 2)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'jns_fig1_national_utilization.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_us_map_per_capita(df_per_capita):
    """Create US choropleth map for per capita TN diagnosis rates."""
    print("Creating US Map: Per Capita TN Diagnosis Rates...")
    
    df = df_per_capita.copy()
    df = df[~df['state'].isin(STATES_TO_EXCLUDE)]
    
    fig = px.choropleth(
        df,
        locations='state_abbrev',
        locationmode='USA-states',
        color='per_100k',
        scope='usa',
        color_continuous_scale='Reds',
        labels={'per_100k': 'TN per 100,000'},
        title='Trigeminal Neuralgia Diagnosis Rate per 100,000 Population'
    )
    
    fig.update_layout(
        geo=dict(bgcolor='white', lakecolor='white'),
        font=dict(family='Arial', size=12),
        title_font_size=14,
        coloraxis_colorbar=dict(title='Per 100,000')
    )
    
    fig.write_image(str(FIGURES_DIR / 'jns_fig_us_map_per_capita.png'), width=1200, height=800, scale=2)
    return fig

def create_us_map_carbamazepine(df_meds):
    """Create US choropleth map for carbamazepine utilization."""
    print("Creating US Map: Carbamazepine Utilization...")
    
    df = df_meds.copy()
    df = df[~df['state'].isin(STATES_TO_EXCLUDE)]
    df['carb_rate'] = df['carbamazepine_oxcarbazepine'] / df['total'] * 100
    df['state_abbrev'] = df['state'].map(STATE_ABBREV)
    
    fig = px.choropleth(
        df,
        locations='state_abbrev',
        locationmode='USA-states',
        color='carb_rate',
        scope='usa',
        color_continuous_scale='Blues',
        labels={'carb_rate': 'Utilization (%)'},
        title='Carbamazepine/Oxcarbazepine Utilization Rate by State'
    )
    
    fig.update_layout(
        geo=dict(bgcolor='white', lakecolor='white'),
        font=dict(family='Arial', size=12),
        title_font_size=14,
        coloraxis_colorbar=dict(title='Rate (%)')
    )
    
    fig.write_image(str(FIGURES_DIR / 'jns_fig_us_map_carbamazepine.png'), width=1200, height=800, scale=2)
    return fig

def create_us_map_mvd(df_procs):
    """Create US choropleth map for MVD utilization."""
    print("Creating US Map: MVD Utilization...")
    
    df = df_procs.copy()
    df = df[~df['state'].isin(STATES_TO_EXCLUDE)]
    df['mvd_rate'] = df['mvd'] / df['total'] * 100
    df['state_abbrev'] = df['state'].map(STATE_ABBREV)
    
    fig = px.choropleth(
        df,
        locations='state_abbrev',
        locationmode='USA-states',
        color='mvd_rate',
        scope='usa',
        color_continuous_scale='Oranges',
        labels={'mvd_rate': 'Utilization (%)'},
        title='Microvascular Decompression (MVD) Utilization Rate by State'
    )
    
    fig.update_layout(
        geo=dict(bgcolor='white', lakecolor='white'),
        font=dict(family='Arial', size=12),
        title_font_size=14,
        coloraxis_colorbar=dict(title='Rate (%)')
    )
    
    fig.write_image(str(FIGURES_DIR / 'jns_fig_us_map_mvd.png'), width=1200, height=800, scale=2)
    return fig

def create_figure2_bar(df_meds):
    """Figure 2: State-Level Carbamazepine Bar Chart (backup)"""
    print("Creating Figure 2: State-Level Carbamazepine Bar Chart...")
    
    df_meds = df_meds[~df_meds['state'].isin(STATES_TO_EXCLUDE)].copy()
    
    df_meds['carb_rate'] = df_meds['carbamazepine_oxcarbazepine'] / df_meds['total'] * 100
    national_rate = df_meds['carbamazepine_oxcarbazepine'].sum() / df_meds['total'].sum() * 100
    
    def get_significance(row):
        z, p = z_test_proportion(row['carbamazepine_oxcarbazepine'], row['total'], national_rate/100)
        return p < 0.05, row['carb_rate'] > national_rate
    
    df_meds[['sig', 'above']] = df_meds.apply(lambda r: pd.Series(get_significance(r)), axis=1)
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    df_sorted = df_meds.sort_values('carb_rate')
    colors = []
    for _, row in df_sorted.iterrows():
        if row['sig'] and row['above']:
            colors.append('#D55E00')
        elif row['sig'] and not row['above']:
            colors.append('#0072B2')
        else:
            colors.append('#999999')
    
    bars = ax.barh(range(len(df_sorted)), df_sorted['carb_rate'], color=colors, edgecolor='black', linewidth=0.3)
    ax.axvline(national_rate, color='black', linestyle='--', linewidth=2, label=f'National Average: {national_rate:.1f}%')
    
    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels(df_sorted['state'], fontsize=8)
    ax.set_xlabel('Carbamazepine/Oxcarbazepine Utilization Rate (%)', fontsize=11)
    ax.set_title('First-Line Medication (Carbamazepine/Oxcarbazepine) Utilization by State', fontsize=12, fontweight='bold')
    
    red_patch = mpatches.Patch(color='#D55E00', label='Significantly Above National Average')
    blue_patch = mpatches.Patch(color='#0072B2', label='Significantly Below National Average')
    gray_patch = mpatches.Patch(color='#999999', label='Not Significantly Different')
    ax.legend(handles=[red_patch, blue_patch, gray_patch], loc='lower right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'jns_fig2_state_carbamazepine_bar.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_figure3_bar(df_procs):
    """Figure 3: State-Level MVD Bar Chart (backup)"""
    print("Creating Figure 3: State-Level MVD Bar Chart...")
    
    df_procs = df_procs[~df_procs['state'].isin(STATES_TO_EXCLUDE)].copy()
    
    df_procs['mvd_rate'] = df_procs['mvd'] / df_procs['total'] * 100
    national_rate = df_procs['mvd'].sum() / df_procs['total'].sum() * 100
    
    def get_significance(row):
        z, p = z_test_proportion(row['mvd'], row['total'], national_rate/100)
        return p < 0.05, row['mvd_rate'] > national_rate
    
    df_procs[['sig', 'above']] = df_procs.apply(lambda r: pd.Series(get_significance(r)), axis=1)
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    df_sorted = df_procs.sort_values('mvd_rate')
    colors = []
    for _, row in df_sorted.iterrows():
        if row['sig'] and row['above']:
            colors.append('#D55E00')
        elif row['sig'] and not row['above']:
            colors.append('#0072B2')
        else:
            colors.append('#999999')
    
    bars = ax.barh(range(len(df_sorted)), df_sorted['mvd_rate'], color=colors, edgecolor='black', linewidth=0.3)
    ax.axvline(national_rate, color='black', linestyle='--', linewidth=2, label=f'National Average: {national_rate:.2f}%')
    
    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels(df_sorted['state'], fontsize=8)
    ax.set_xlabel('MVD Utilization Rate (%)', fontsize=11)
    ax.set_title('Microvascular Decompression (MVD) Utilization by State', fontsize=12, fontweight='bold')
    
    red_patch = mpatches.Patch(color='#D55E00', label='Significantly Above National Average')
    blue_patch = mpatches.Patch(color='#0072B2', label='Significantly Below National Average')
    gray_patch = mpatches.Patch(color='#999999', label='Not Significantly Different')
    ax.legend(handles=[red_patch, blue_patch, gray_patch], loc='lower right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'jns_fig3_state_mvd_bar.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_figure4_heatmap(df_meds, df_procs):
    """Figure 4: Combined Regional Treatment Heatmap"""
    print("Creating Figure 4: Regional Treatment Heatmap...")
    
    med_cols = ['carbamazepine_oxcarbazepine', 'gabapentin', 'pregabalin', 'baclofen', 'lamotrigine']
    proc_cols = ['mvd', 'srs', 'rhizotomy', 'botox']
    
    region_meds = df_meds.groupby('census_region').agg({
        **{col: 'sum' for col in med_cols if col in df_meds.columns},
        'total': 'sum'
    }).reset_index()
    
    region_procs = df_procs.groupby('census_region').agg({
        **{col: 'sum' for col in proc_cols if col in df_procs.columns},
        'total': 'sum'
    }).reset_index()
    
    for col in med_cols:
        if col in region_meds.columns:
            region_meds[col] = region_meds[col] / region_meds['total'] * 100
    
    for col in proc_cols:
        if col in region_procs.columns:
            region_procs[col] = region_procs[col] / region_procs['total'] * 100
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    med_matrix = region_meds.set_index('census_region')[med_cols]
    med_matrix.columns = ['Carb/Oxcarb', 'Gabapentin', 'Pregabalin', 'Baclofen', 'Lamotrigine']
    
    ax1 = axes[0]
    sns.heatmap(med_matrix, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax1,
                cbar_kws={'label': 'Rate (%)'}, linewidths=0.5)
    ax1.set_title('A. Medication Utilization by Region (%)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    
    proc_matrix = region_procs.set_index('census_region')[proc_cols]
    proc_matrix.columns = ['MVD', 'SRS', 'Rhizotomy', 'Botox']
    
    ax2 = axes[1]
    sns.heatmap(proc_matrix, annot=True, fmt='.2f', cmap='YlGnBu', ax=ax2,
                cbar_kws={'label': 'Rate (%)'}, linewidths=0.5)
    ax2.set_title('B. Surgical Procedure Utilization by Region (%)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('')
    ax2.set_ylabel('')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'jns_fig4_regional_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_figure5_pathways(df_cross):
    """Figure 5: Treatment Escalation Pathways"""
    print("Creating Figure 5: Treatment Escalation Pathways...")
    
    df_national = df_cross.groupby('medication').agg({
        'mvd': 'sum',
        'srs': 'sum',
        'rhizotomy': 'sum',
        'botox': 'sum',
        'total': 'sum'
    }).reset_index()
    
    proc_cols = ['mvd', 'srs', 'rhizotomy', 'botox']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(df_national))
    width = 0.2
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, proc in enumerate(proc_cols):
        rates = df_national[proc] / df_national['total'] * 100
        bars = ax.bar(x + i * width, rates, width, label=proc.upper(), color=colors[i], edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Medication Group', fontsize=11)
    ax.set_ylabel('Procedure Rate (%)', fontsize=11)
    ax.set_title('Surgical Procedure Rates by Medication Group', fontsize=12, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    
    med_labels = {
        'carbamazepine_oxcarbazepine': 'Carb/Oxcarb',
        'gabapentin': 'Gabapentin',
        'pregabalin': 'Pregabalin',
        'baclofen': 'Baclofen',
        'lamotrigine': 'Lamotrigine',
        'none_of_above': 'No TN Med'
    }
    ax.set_xticklabels([med_labels.get(m, m) for m in df_national['medication']], rotation=45, ha='right')
    ax.legend(loc='upper right')
    ax.set_ylim(0, 5)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'jns_fig5_treatment_pathways.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def main():
    print("=" * 70)
    print("Generating Publication Materials for JNS")
    print("=" * 70)
    
    # Load data
    print("\nLoading data...")
    df_meds = pd.read_csv(DATA_DIR / 'state_medications_clean.csv')
    df_procs = pd.read_csv(DATA_DIR / 'state_procedures_clean.csv')
    df_cross = pd.read_csv(DATA_DIR / 'state_meds_procedures_clean.csv')
    
    print(f"  Medications: {df_meds.shape}")
    print(f"  Procedures: {df_procs.shape}")
    print(f"  Cross-tab: {df_cross.shape}")
    
    # Create tables
    print("\n" + "=" * 70)
    print("CREATING TABLES")
    print("=" * 70)
    
    table1 = create_table1(df_meds)
    df_per_capita = create_table_per_capita(df_meds)
    table2 = create_table2(df_meds, df_procs)
    table3 = create_table3(df_meds, df_procs)
    table4 = create_table4(df_meds, df_procs)
    
    # Create figures
    print("\n" + "=" * 70)
    print("CREATING FIGURES")
    print("=" * 70)
    
    create_figure1(df_meds, df_procs)
    
    # US Map visualizations
    create_us_map_per_capita(df_per_capita)
    create_us_map_carbamazepine(df_meds.copy())
    create_us_map_mvd(df_procs.copy())
    
    # Bar charts (supplementary)
    create_figure2_bar(df_meds.copy())
    create_figure3_bar(df_procs.copy())
    
    create_figure4_heatmap(df_meds, df_procs)
    create_figure5_pathways(df_cross)
    
    print("\n" + "=" * 70)
    print("✓ All materials generated successfully!")
    print("=" * 70)
    
    return {
        'tables': [table1, df_per_capita, table2, table3, table4],
        'figures': [
            'jns_fig1_national_utilization.png',
            'jns_fig_us_map_per_capita.png',
            'jns_fig_us_map_carbamazepine.png',
            'jns_fig_us_map_mvd.png',
            'jns_fig2_state_carbamazepine_bar.png',
            'jns_fig3_state_mvd_bar.png',
            'jns_fig4_regional_heatmap.png',
            'jns_fig5_treatment_pathways.png'
        ]
    }

if __name__ == "__main__":
    main()
