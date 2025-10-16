# Notebooks Directory

Jupyter notebooks for requirements analysis and experimentation.

## Files

### `SMART_analyzer.ipynb`
**Main ISO/IEC/IEEE 29148 analyzer notebook**

- Parses RDF/Turtle requirement files
- Analyzes requirements using Azure OpenAI (o3-mini-1)
- Evaluates 8 ISO 29148 quality criteria
- Exports to Excel with 2 sheets (detailed + parent summary)

**Usage:**
```python
INPUT_FILE_PATH = '../data/input/NVD110_VS2_20250709.txt'
OUTPUT_FILE_PATH = '../data/output/SMART_analysis_results.xlsx'
MAX_REQUIREMENTS_TO_ANALYZE = 50  # or None for all
```

**Key Features:**
- Concurrent batch processing (15 workers)
- Parent-child relationship analysis
- Quality score (0-8) per requirement
- Improvement suggestions in Dutch

---

### `relationships.ipynb`
**Requirement relationship analyzer**

- Explores parent-child relationships in requirements
- Visualizes requirement hierarchies
- Analyzes dependency patterns

---

### `unscructured_data_analyzer.ipynb`
**Unstructured data processing**

- Parses contracts and text documents
- Extracts requirements from unstructured text
- Text preprocessing and cleaning

## Running Notebooks

### Prerequisites
```bash
pip install -r requirements.txt
```

### Jupyter Setup
```bash
jupyter notebook
# or
jupyter lab
```

### Environment Variables
Notebooks use environment variables for Azure OpenAI:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_MODEL_NAME`

These are automatically loaded from the `.env` file in the project root.

## Output

All notebook outputs are saved to `../data/output/`

## Notes

- Notebooks use relative paths to `../data/` folders
- API credentials are loaded from `.env` file
- Large files are not tracked in git
