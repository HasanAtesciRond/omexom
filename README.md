# ISO/IEC/IEEE 29148 Requirements Quality Analyzer

A professional web application for analyzing requirements quality based on the ISO/IEC/IEEE 29148 international standard.

## 🎯 Overview

This project provides both a **Streamlit web application** and **Jupyter notebooks** for analyzing requirements from RDF/Turtle files. It uses Azure OpenAI to evaluate requirements against 8 quality criteria defined in ISO/IEC/IEEE 29148.

## 📁 Project Structure

```
omexom/
├── streamlit_app.py              # Main Streamlit app entry point
├── pages/                        # Streamlit app pages (7 pages)
│   ├── 1_📤_Upload.py
│   ├── 2_⚙️_Analysis.py
│   ├── 3_📊_Dashboard.py
│   ├── 4_📋_Results.py
│   ├── 5_🔍_Criteria.py
│   ├── 6_🌳_Hierarchy.py
│   └── 7_💾_Export.py
├── utils/                        # Core utilities
│   ├── rdf_parser.py            # RDF/Turtle parsing
│   ├── analyzer.py              # Azure OpenAI integration
│   ├── visualizations.py        # Plotly charts
│   └── export_utils.py          # Export functions
├── config/                       # Configuration
│   ├── settings.py              # App settings
│   └── criteria_definitions.py  # ISO 29148 criteria
├── data/                         # Data files (see data/README.md)
│   ├── input/                   # Input RDF/Turtle files
│   ├── output/                  # Analysis results
│   └── examples/                # Example files
├── notebooks/                    # Jupyter notebooks (see notebooks/README.md)
│   ├── SMART_analyzer.ipynb
│   ├── relationships.ipynb
│   └── unscructured_data_analyzer.ipynb
├── docs/                         # Documentation (see docs/README.md)
│   ├── PRD.md                   # Product Requirements
│   ├── QUICK_START.md           # Quick start guide
│   ├── STREAMLIT_README.md      # Full documentation
│   └── TEST_RESULTS.md          # Test reports
├── tests/                        # Test files (see tests/README.md)
│   └── test_analyzer.py
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Jupyter notebook dependencies
└── streamlit_requirements.txt    # Streamlit app dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git

### Installation

#### Option A: Using pip (Recommended for most users)

```bash
# 1. Clone the repository
git clone https://github.com/HasanAtesciRond/omexom.git
cd omexom

# 2. Create a virtual environment (IMPORTANT: avoid conda/pip conflicts)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your Azure OpenAI credentials
# Copy .env.example to .env and fill in your credentials

# 5. Run the Streamlit app
streamlit run streamlit_app.py

# 6. Open browser to http://localhost:8501
```

#### Option B: Using Conda

```bash
# 1. Clone the repository
git clone https://github.com/HasanAtesciRond/omexom.git
cd omexom

# 2. Create conda environment from environment.yml
conda env create -f environment.yml

# 3. Activate the environment
conda activate omexom-iso29148

# 4. Create .env file with your Azure OpenAI credentials
# Copy .env.example to .env and fill in your credentials

# 5. Run the Streamlit app
streamlit run streamlit_app.py

# 6. Open browser to http://localhost:8501
```

### Running Jupyter Notebooks

```bash
# After completing installation steps above:

# 1. Start Jupyter
jupyter notebook

# 2. Open notebooks/SMART_analyzer.ipynb
```

### Important Notes

- **DO NOT mix pip and conda**: Choose one installation method and stick with it
- **Always use a virtual environment**: This prevents conflicts with your base Python installation
- **requirements.txt uses flexible version ranges**: Compatible with different Python versions (3.9-3.12)

## 📊 Features

### Streamlit Web App
- ✅ Upload RDF/Turtle requirement files
- ✅ Parse 668+ requirements with parent-child relationships
- ✅ AI-powered ISO 29148 quality analysis
- ✅ Interactive dashboards with Plotly visualizations
- ✅ Filter and search through results
- ✅ Per-criterion deep-dive analysis
- ✅ Hierarchy tree visualization
- ✅ Export to Excel, CSV, JSON

### 8 ISO 29148 Quality Criteria
1. ✅ **Necessary** (Noodzakelijk)
2. 🎯 **Unambiguous** (Eenduidig)
3. 📋 **Complete** (Compleet)
4. 1️⃣ **Singular** (Enkelvoudig)
5. 🔧 **Feasible** (Haalbaar)
6. ✔️ **Verifiable** (Verifieerbaar)
7. 🔗 **Traceable** (Traceerbaar)
8. 🎨 **Implementation-free** (Implementatie-onafhankelijk)

## 📖 Documentation

- **Quick Start:** [docs/QUICK_START.md](docs/QUICK_START.md)
- **Full Documentation:** [docs/STREAMLIT_README.md](docs/STREAMLIT_README.md)
- **Product Spec:** [docs/PRD.md](docs/PRD.md)
- **Test Results:** [docs/TEST_RESULTS.md](docs/TEST_RESULTS.md)

## 🔧 Configuration

### Automatic (Recommended)
Credentials are automatically loaded from `.env` file:
```env
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_MODEL_NAME=o3-mini-1
```

### Manual
Configure via Streamlit UI sidebar after app starts.

## 📊 Performance

- **Parse Time:** < 2 seconds for 668 requirements
- **Analysis Time:** ~2-3 seconds per requirement (API dependent)
- **Scalability:** Up to 10,000 requirements
- **Concurrent Workers:** 15 (configurable)

## 🧪 Testing

```bash
# Run quick test
python tests/test_analyzer.py

# Expected: 2 requirements analyzed successfully
```

See [tests/README.md](tests/README.md) for details.

## 📝 Data

### Input Files
Place RDF/Turtle files in `data/input/`:
- `NVD110_VS2_20250709.txt` (668 requirements)
- Other `.txt` or `.ttl` files with NEN2660 requirements

### Output Files
Analysis results saved to `data/output/`:
- `SMART_analysis_results.xlsx` (2 sheets: detailed + summary)
- `ISO29148_Analysis_*.xlsx` (Streamlit exports)
- CSV and JSON formats available

See [data/README.md](data/README.md) for details.

## 🔒 Security

- ✅ API keys in `.env` (not tracked in git)
- ✅ `.gitignore` protects sensitive files
- ✅ No data persistence (session-only in Streamlit)
- ✅ Local processing only

## 🗺️ Roadmap

- [x] ISO 29148 criteria implementation
- [x] Streamlit web interface
- [x] Parent-child relationship analysis
- [x] Multi-format export
- [ ] PDF reports with charts
- [ ] Historical comparison
- [ ] Custom criteria weights
- [ ] User authentication
- [ ] Jira/Azure DevOps integration

## 📄 License

Proprietary - Omexom Internal Use Only

## 👥 Contact

For questions or support, contact the development team.

---

**Version:** 1.0.0
**Last Updated:** 2025-10-16
**Status:** Production Ready
