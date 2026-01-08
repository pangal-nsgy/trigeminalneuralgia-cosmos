"""
Data Cleaning Utilities for Cosmos Data Pipeline
=================================================

This module provides reusable functions for cleaning and processing
Epic Cosmos data exports. Designed to handle common issues like:
- Multi-row headers
- "10 or fewer" privacy masking
- Inconsistent column naming
- Data validation

Author: Stanford Neurosurgery Research
Date: January 2026
"""

import pandas as pd
import numpy as np
from typing import Union, List, Optional, Tuple, Dict
from pathlib import Path
import warnings

# Import configuration
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.config import SMALL_CELL_VALUE, SMALL_CELL_IMPUTATION, STATE_TO_REGION


# =============================================================================
# CORE CLEANING FUNCTIONS
# =============================================================================

def impute_small_cells(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    small_cell_value: str = SMALL_CELL_VALUE,
    imputation_value: int = SMALL_CELL_IMPUTATION
) -> pd.DataFrame:
    """
    Impute "10 or fewer" values with a specified value (default: 5).
    
    IMPORTANT: This is a documented decision for privacy-protected cells.
    The midpoint value of 5 is a conservative estimate for aggregate analyses.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing data with small cell values
    columns : List[str], optional
        Specific columns to process. If None, processes all columns.
    small_cell_value : str
        The string indicating a small cell (default: "10 or fewer")
    imputation_value : int
        Value to replace small cells with (default: 5)
        
    Returns
    -------
    pd.DataFrame
        DataFrame with imputed values
        
    Notes
    -----
    Imputation decision documented per IRB protocol.
    Midpoint of [1, 10] range = 5.5, rounded to 5.
    """
    df = df.copy()
    
    if columns is None:
        columns = df.columns.tolist()
    
    for col in columns:
        if col in df.columns:
            # Replace string "10 or fewer" with imputation value
            df[col] = df[col].replace(small_cell_value, imputation_value)
            
            # Try to convert to numeric
            df[col] = pd.to_numeric(df[col], errors='ignore')
    
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to snake_case.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns to clean
        
    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned column names
    """
    df = df.copy()
    
    # Clean column names
    new_columns = []
    for col in df.columns:
        # Convert to string
        col_str = str(col)
        # Replace spaces and special chars with underscore
        col_str = col_str.lower()
        col_str = col_str.replace(' ', '_')
        col_str = col_str.replace('-', '_')
        col_str = col_str.replace('/', '_')
        col_str = col_str.replace('(', '')
        col_str = col_str.replace(')', '')
        col_str = col_str.replace(',', '')
        col_str = col_str.replace('.', '')
        # Remove consecutive underscores
        while '__' in col_str:
            col_str = col_str.replace('__', '_')
        # Remove leading/trailing underscores
        col_str = col_str.strip('_')
        new_columns.append(col_str)
    
    df.columns = new_columns
    return df


def extract_epic_data(
    filepath: Union[str, Path],
    header_row: int = 10,
    sheet_name: Union[str, int] = 0
) -> pd.DataFrame:
    """
    Extract data from Epic Cosmos Excel export, skipping metadata headers.
    
    Parameters
    ----------
    filepath : str or Path
        Path to Excel file
    header_row : int
        Row number (0-indexed) where actual column headers begin
    sheet_name : str or int
        Sheet to read (default: first sheet)
        
    Returns
    -------
    pd.DataFrame
        Extracted data with proper headers
    """
    # Read the full file first to inspect structure
    df_raw = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
    
    # Find the header row - look for row with meaningful column names
    # Epic exports typically have headers after metadata rows
    header_idx = header_row
    
    # Extract column names from header row
    headers = df_raw.iloc[header_idx].tolist()
    
    # Get data starting from row after header
    df = df_raw.iloc[header_idx + 1:].copy()
    df.columns = headers
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Remove rows that are all NaN
    df = df.dropna(how='all')
    
    return df


def add_census_region(
    df: pd.DataFrame,
    state_column: str = 'state'
) -> pd.DataFrame:
    """
    Add census region column based on state.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with state column
    state_column : str
        Name of the state column
        
    Returns
    -------
    pd.DataFrame
        DataFrame with added 'census_region' column
    """
    df = df.copy()
    df['census_region'] = df[state_column].map(STATE_TO_REGION)
    return df


# =============================================================================
# MEDICATION DATA CLEANING
# =============================================================================

def clean_medication_data(
    df: pd.DataFrame,
    state_col: str = 'State of Residence',
    medication_col: str = 'All Medications',
    count_col: str = None
) -> pd.DataFrame:
    """
    Clean medication data from Epic Cosmos export.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw medication data
    state_col : str
        Name of state column
    medication_col : str
        Name of medication column
    count_col : str
        Name of count column (if None, inferred)
        
    Returns
    -------
    pd.DataFrame
        Cleaned medication data in tidy format
    """
    df = df.copy()
    
    # Forward fill state names (Epic exports have merged cells)
    if state_col in df.columns:
        df[state_col] = df[state_col].ffill()
    
    # Identify count column if not specified
    if count_col is None:
        # Look for numeric or "10 or fewer" columns
        for col in df.columns:
            if col not in [state_col, medication_col]:
                # Check if column contains counts
                sample = df[col].dropna().head(10)
                if any(isinstance(x, (int, float)) or x == SMALL_CELL_VALUE for x in sample):
                    count_col = col
                    break
    
    # Standardize medication names
    medication_mapping = {
        'Carbmazapine or Oxcarbmazapine': 'Carbamazepine/Oxcarbazepine',
        'Carbamazepine or Oxcarbazepine': 'Carbamazepine/Oxcarbazepine',
        'baclofen': 'Baclofen',
        'gabapentin': 'Gabapentin',
        'lamotrigine': 'Lamotrigine',
        'pregabalin': 'Pregabalin',
        'onabotulinumtoxinA': 'OnabotulinumtoxinA',
        'None of the above': 'None of the above'
    }
    
    if medication_col in df.columns:
        df[medication_col] = df[medication_col].replace(medication_mapping)
    
    return df


# =============================================================================
# PROCEDURE DATA CLEANING
# =============================================================================

def clean_procedure_data(
    df: pd.DataFrame,
    state_col: str = 'State of Residence'
) -> pd.DataFrame:
    """
    Clean procedure data from Epic Cosmos export.
    
    Handles CPT code descriptions and standardizes procedure names.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw procedure data
    state_col : str
        Name of state column
        
    Returns
    -------
    pd.DataFrame
        Cleaned procedure data
    """
    df = df.copy()
    
    # Forward fill state names
    if state_col in df.columns:
        df[state_col] = df[state_col].ffill()
    
    # Standardize procedure column names
    procedure_mapping = {
        'CRNEC SOPL EXPLORATION/DECOMPRESSION CRANIAL NRV 61458': 'MVD',
        'SRS 61796 and 98': 'SRS',
        'CREATE LESION STRTCTC PRQ NEUROLYTIC GASSERIAN 61790': 'Rhizotomy',
        'Glycerol Rhizotomy': 'Glycerol Rhizotomy',
        'CHEMODNRVTJ MUSC MUSC INNERVATED FACIAL NRV UNIL 64612': 'Botox',
        'None of the above': 'None of the above'
    }
    
    # Apply mapping to column names if they contain CPT descriptions
    new_columns = []
    for col in df.columns:
        if col in procedure_mapping:
            new_columns.append(procedure_mapping[col])
        else:
            new_columns.append(col)
    df.columns = new_columns
    
    return df


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_totals(
    df: pd.DataFrame,
    value_columns: List[str],
    group_column: str = None,
    expected_total: int = None,
    tolerance: float = 0.05
) -> Tuple[bool, Dict]:
    """
    Validate that row/column totals match expected values.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate
    value_columns : List[str]
        Columns containing numeric values to sum
    group_column : str, optional
        Column to group by for subtotals
    expected_total : int, optional
        Expected grand total
    tolerance : float
        Acceptable percentage difference from expected
        
    Returns
    -------
    Tuple[bool, Dict]
        (is_valid, details_dict)
    """
    results = {
        'calculated_total': 0,
        'expected_total': expected_total,
        'difference': None,
        'percent_difference': None,
        'issues': []
    }
    
    # Calculate totals
    total = 0
    for col in value_columns:
        if col in df.columns:
            col_sum = pd.to_numeric(df[col], errors='coerce').sum()
            total += col_sum
    
    results['calculated_total'] = total
    
    if expected_total is not None:
        diff = abs(total - expected_total)
        results['difference'] = diff
        results['percent_difference'] = (diff / expected_total) * 100 if expected_total > 0 else 0
        
        if results['percent_difference'] > tolerance * 100:
            results['issues'].append(
                f"Total differs by {results['percent_difference']:.2f}% from expected"
            )
    
    is_valid = len(results['issues']) == 0
    return is_valid, results


def check_missing_states(
    df: pd.DataFrame,
    state_column: str = 'state'
) -> List[str]:
    """
    Check for missing US states in the data.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with state data
    state_column : str
        Name of state column
        
    Returns
    -------
    List[str]
        List of missing states
    """
    all_states = set(STATE_TO_REGION.keys())
    present_states = set(df[state_column].dropna().unique())
    missing = all_states - present_states
    return sorted(list(missing))


# =============================================================================
# DATA TRANSFORMATION FUNCTIONS
# =============================================================================

def pivot_to_wide(
    df: pd.DataFrame,
    index_col: str,
    columns_col: str,
    values_col: str
) -> pd.DataFrame:
    """
    Pivot long-form data to wide format.
    
    Parameters
    ----------
    df : pd.DataFrame
        Long-form DataFrame
    index_col : str
        Column to use as index (e.g., 'state')
    columns_col : str
        Column whose values become new columns (e.g., 'medication')
    values_col : str
        Column containing values (e.g., 'count')
        
    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame
    """
    return df.pivot_table(
        index=index_col,
        columns=columns_col,
        values=values_col,
        aggfunc='sum'
    ).reset_index()


def melt_to_long(
    df: pd.DataFrame,
    id_vars: List[str],
    value_vars: List[str],
    var_name: str = 'variable',
    value_name: str = 'value'
) -> pd.DataFrame:
    """
    Melt wide-form data to long format.
    
    Parameters
    ----------
    df : pd.DataFrame
        Wide-form DataFrame
    id_vars : List[str]
        Columns to keep as identifiers
    value_vars : List[str]
        Columns to unpivot
    var_name : str
        Name for the variable column
    value_name : str
        Name for the value column
        
    Returns
    -------
    pd.DataFrame
        Long-format DataFrame
    """
    return pd.melt(
        df,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name=var_name,
        value_name=value_name
    )


def calculate_percentages(
    df: pd.DataFrame,
    count_col: str,
    total_col: str = None,
    group_col: str = None
) -> pd.DataFrame:
    """
    Calculate percentages from counts.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with count data
    count_col : str
        Column containing counts
    total_col : str, optional
        Column containing totals. If None, calculates from group.
    group_col : str, optional
        Column to group by for calculating totals
        
    Returns
    -------
    pd.DataFrame
        DataFrame with added 'percentage' column
    """
    df = df.copy()
    
    if total_col is not None:
        df['percentage'] = (df[count_col] / df[total_col]) * 100
    elif group_col is not None:
        totals = df.groupby(group_col)[count_col].transform('sum')
        df['percentage'] = (df[count_col] / totals) * 100
    else:
        total = df[count_col].sum()
        df['percentage'] = (df[count_col] / total) * 100
    
    return df

