# Data Directory

This folder contains all data files for the ISO 29148 Requirements Analyzer.

## Structure

```
data/
├── input/          # Input RDF/Turtle requirement files
├── output/         # Analysis results and exports
└── examples/       # Example files and databases
```

## Folders

### `input/`
Contains RDF/Turtle (`.txt`, `.ttl`) files with requirements in NEN2660 format.

**Current files:**
- `NVD110_VS2_20250709.txt` - Main requirements file (668 requirements)
- `003.350.00 1568348 NVD-OMX-AANB-VS1-A01.txt` - Alternative requirements set
- Additional TTL format files

### `output/`
Contains analysis results from the Streamlit app and Jupyter notebooks.

**Generated files:**
- `SMART_analysis_results.xlsx` - ISO 29148 analysis results
- `ISO29148_Analysis_*.xlsx` - Streamlit app exports
- `*.csv`, `*.json` - Alternative export formats
- `parsed_contract_text.txt` - Parsed text from contracts

### `examples/`
Example files and reference databases.

**Files:**
- `Contract_voorbeeld.pdf` - Example contract
- `Omexom Database 26-08-2025.xlsx` - Reference database

## Usage

### For Streamlit App:
1. Upload files from `input/` folder via the app UI
2. Results are saved to `output/` folder

### For Jupyter Notebooks:
```python
INPUT_FILE_PATH = 'data/input/NVD110_VS2_20250709.txt'
OUTPUT_FILE_PATH = 'data/output/SMART_analysis_results.xlsx'
```

## Git Tracking

- `input/` files are **NOT tracked** (too large)
- `output/` files are **NOT tracked** (generated)
- `examples/` folder structure is tracked
- See `.gitignore` for details
