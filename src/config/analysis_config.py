"""
Analysis Configuration for Cosmos Data Pipeline
================================================

This module contains all configuration parameters for the TN (Trigeminal Neuralgia)
analysis pipeline. Designed to be modular for reuse with other pathologies.

Author: Stanford Neurosurgery Research
Date: January 2026
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Project root - dynamically determined
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
RAW_DATA_DIR = PROJECT_ROOT / "TN_Data"
PROCESSED_DATA_DIR = PROJECT_ROOT / "analysis" / "outputs" / "data"
TABLES_DIR = PROJECT_ROOT / "analysis" / "outputs" / "tables"
FIGURES_DIR = PROJECT_ROOT / "analysis" / "outputs" / "figures"
NOTEBOOKS_DIR = PROJECT_ROOT / "analysis" / "notebooks"

# =============================================================================
# DATA IMPUTATION SETTINGS
# =============================================================================

# IMPORTANT: Privacy-protected values "10 or fewer" are imputed as 5 (midpoint)
# This is a conservative estimate for aggregated analyses
# Documented per research protocol
SMALL_CELL_VALUE = "10 or fewer"
SMALL_CELL_IMPUTATION = 5

# =============================================================================
# JOURNAL FORMATTING - JNS (Journal of Neurosurgery)
# =============================================================================

@dataclass
class JNSFormatting:
    """Journal of Neurosurgery formatting standards."""
    
    # Table formatting
    decimal_places: int = 1  # For percentages
    ci_decimal_places: int = 1  # For confidence intervals
    p_value_threshold: float = 0.05
    p_value_format: str = "<0.001"  # For very small p-values
    
    # Figure settings
    figure_dpi: int = 300
    figure_format: str = "tiff"  # JNS prefers TIFF
    max_figure_width_inches: float = 7.0  # Single column
    max_figure_width_full: float = 14.0  # Double column
    
    # Font settings
    font_family: str = "Arial"
    font_size_axis: int = 10
    font_size_title: int = 12
    font_size_legend: int = 9
    
    # Color palette (colorblind-friendly)
    colors: List[str] = field(default_factory=lambda: [
        "#0072B2",  # Blue
        "#D55E00",  # Orange
        "#009E73",  # Green
        "#CC79A7",  # Pink
        "#F0E442",  # Yellow
        "#56B4E9",  # Light blue
        "#E69F00",  # Gold
        "#000000",  # Black
    ])

JNS = JNSFormatting()

# =============================================================================
# TRIGEMINAL NEURALGIA SPECIFIC CONFIGURATION
# =============================================================================

@dataclass
class TNConfig:
    """Configuration specific to Trigeminal Neuralgia analysis."""
    
    # ICD-10 Code
    icd10_code: str = "G50.0"
    condition_name: str = "Trigeminal Neuralgia"
    condition_abbreviation: str = "TN"
    
    # Study period
    study_start: str = "2022-11-28"
    study_end: str = "2025-11-27"
    study_duration_years: int = 3
    
    # Data source
    data_source: str = "Epic Cosmos"
    
    # Medications of interest (in clinical priority order)
    medications: Dict[str, str] = field(default_factory=lambda: {
        "carbamazepine_oxcarbazepine": "Carbamazepine/Oxcarbazepine",
        "gabapentin": "Gabapentin",
        "pregabalin": "Pregabalin",
        "baclofen": "Baclofen",
        "lamotrigine": "Lamotrigine",
        "botox": "OnabotulinumtoxinA",
        "none": "None of the above"
    })
    
    # Medications display order (for tables/figures)
    medication_order: List[str] = field(default_factory=lambda: [
        "Carbamazepine/Oxcarbazepine",  # First-line
        "Gabapentin",
        "Pregabalin", 
        "Baclofen",
        "Lamotrigine",
        "OnabotulinumtoxinA",
        "None of the above"
    ])
    
    # Procedures of interest (in clinical order)
    procedures: Dict[str, str] = field(default_factory=lambda: {
        "mvd": "MVD (Microvascular Decompression)",
        "srs": "SRS (Stereotactic Radiosurgery)",
        "rhizotomy": "Percutaneous Rhizotomy",
        "glycerol": "Glycerol Rhizotomy",
        "botox": "Botox Injection",
        "none": "None of the above"
    })
    
    # CPT codes for reference
    cpt_codes: Dict[str, str] = field(default_factory=lambda: {
        "mvd": "61458",
        "srs": "61796",
        "rhizotomy": "61790",
        "botox": "64612"
    })
    
    # Procedures display order
    procedure_order: List[str] = field(default_factory=lambda: [
        "MVD",
        "SRS",
        "Rhizotomy",
        "Glycerol Rhizotomy",
        "Botox",
        "None of the above"
    ])

TN_CONFIG = TNConfig()

# =============================================================================
# STATES TO EXCLUDE FROM STATE-LEVEL ANALYSIS
# =============================================================================

# States with very small sample sizes (n < 10) that create unreliable percentages
# These are excluded from state-level visualizations but included in national/regional totals
STATES_TO_EXCLUDE = [
    "Alaska",  # < 10 patients; extreme percentage outliers
]

# =============================================================================
# US CENSUS REGIONS
# =============================================================================

CENSUS_REGIONS = {
    "East North Central": ["Ohio", "Michigan", "Illinois", "Wisconsin", "Indiana"],
    "West North Central": ["Minnesota", "Iowa", "Missouri", "Kansas", "Nebraska", 
                           "North Dakota", "South Dakota"],
    "Middle Atlantic": ["Pennsylvania", "New York", "New Jersey"],
    "New England": ["Massachusetts", "Connecticut", "Maine", "New Hampshire", 
                    "Rhode Island", "Vermont"],
    "South Atlantic": ["Florida", "North Carolina", "Virginia", "South Carolina", 
                       "Georgia", "Maryland", "West Virginia", "Delaware", 
                       "District of Columbia"],
    "East South Central": ["Kentucky", "Mississippi", "Tennessee", "Alabama"],
    "West South Central": ["Texas", "Louisiana", "Arkansas", "Oklahoma"],
    "Pacific": ["California", "Oregon", "Washington", "Hawaii", "Alaska"],
    "Mountain": ["Colorado", "Arizona", "Utah", "Idaho", "Nevada", "Montana", 
                 "New Mexico", "Wyoming"]
}

# Reverse mapping: state -> region
STATE_TO_REGION = {}
for region, states in CENSUS_REGIONS.items():
    for state in states:
        STATE_TO_REGION[state] = region

# =============================================================================
# DATA FILE CONFIGURATION
# =============================================================================

@dataclass
class DataFiles:
    """Configuration for raw data files."""
    
    # State-level files
    medications_by_state: str = "TN Medication Data.xlsx"
    procedures_by_state: str = "TN procedures only.xlsx"
    meds_procedures_by_state: str = "TN meds and procedures.xlsx"
    
    # Census region files (aggregated to avoid small-cell suppression)
    medications_by_census: str = "Meds and Census Jan 4 2026.xlsx"
    procedures_by_census: str = "Procedures and Census.xlsx"
    meds_procedures_by_census: str = "TN meds then procedures by census Jan 4 2026.xlsx"
    
    # Header rows to skip in Epic exports
    header_rows_to_skip: int = 10  # Metadata rows before actual data

DATA_FILES = DataFiles()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_file_path(filename: str, raw: bool = True) -> Path:
    """Get full path to a data file."""
    if raw:
        return RAW_DATA_DIR / filename
    return PROCESSED_DATA_DIR / filename


def ensure_directories():
    """Create output directories if they don't exist."""
    for directory in [PROCESSED_DATA_DIR, TABLES_DIR, FIGURES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


# =============================================================================
# PIPELINE CONFIGURATION (for reuse with other pathologies)
# =============================================================================

@dataclass
class PipelineConfig:
    """
    Generic pipeline configuration.
    Extend this for other pathologies by creating new config instances.
    """
    condition_name: str
    condition_abbreviation: str
    icd10_code: str
    medications: Dict[str, str]
    procedures: Dict[str, str]
    study_start: str
    study_end: str
    
    # Imputation settings
    small_cell_value: str = "10 or fewer"
    small_cell_imputation: int = 5
    
    def __post_init__(self):
        """Validate configuration."""
        if not self.medications:
            raise ValueError("At least one medication must be specified")
        if not self.procedures:
            raise ValueError("At least one procedure must be specified")


# Current analysis configuration
CURRENT_CONFIG = PipelineConfig(
    condition_name=TN_CONFIG.condition_name,
    condition_abbreviation=TN_CONFIG.condition_abbreviation,
    icd10_code=TN_CONFIG.icd10_code,
    medications=TN_CONFIG.medications,
    procedures=TN_CONFIG.procedures,
    study_start=TN_CONFIG.study_start,
    study_end=TN_CONFIG.study_end
)

