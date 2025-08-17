# src/paths.py
from pathlib import Path

# ---------- Root Directories ----------
# Dataset is expected to be in the project root under "data/raw"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = PROJECT_ROOT / "data" / "raw"

# ---------- Subdirectories ----------
ORIGINAL_DIR = DATASET_ROOT / "original"
ALTERED_EASY_DIR = DATASET_ROOT / "Altered_Easy"
ALTERED_MEDIUM_DIR = DATASET_ROOT / "Altered_Medium"
ALTERED_HARD_DIR = DATASET_ROOT / "Altered_Hard"

# ---------- Project Outputs ----------
METADATA_CSV = PROJECT_ROOT / "metadata.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = PROJECT_ROOT / "models"

# Ensure output folders exist
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
