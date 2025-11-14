"""
ISO/IEC/IEEE 29148 Requirements Quality Analyzer
Main Streamlit Application Entry Point
"""

import streamlit as st
import os
from dotenv import load_dotenv
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT, SESSION_KEYS

# Load environment variables from .env file
load_dotenv()

# st.sidebar.image("Omexom-site-corp@2x-1.webp")
# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

st.image("Omexom-site-corp@2x-1.webp")


# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if SESSION_KEYS['uploaded_file'] not in st.session_state:
        st.session_state[SESSION_KEYS['uploaded_file']] = None

    if SESSION_KEYS['uploaded_filename'] not in st.session_state:
        st.session_state[SESSION_KEYS['uploaded_filename']] = None

    if SESSION_KEYS['requirements'] not in st.session_state:
        st.session_state[SESSION_KEYS['requirements']] = None

    if SESSION_KEYS['analysis_results'] not in st.session_state:
        st.session_state[SESSION_KEYS['analysis_results']] = None

    if SESSION_KEYS['analyzer_config'] not in st.session_state:
        # Load from environment variables (from .env file) or Streamlit secrets
        # Try to get from secrets, but fallback gracefully if not available
        try:
            secrets_azure = st.secrets.get('azure_openai', {})
            secrets_analysis = st.secrets.get('analysis', {})
        except:
            secrets_azure = {}
            secrets_analysis = {}

        st.session_state[SESSION_KEYS['analyzer_config']] = {
            'azure_endpoint': os.getenv('AZURE_OPENAI_ENDPOINT', secrets_azure.get('endpoint', '')),
            'api_key': os.getenv('AZURE_OPENAI_API_KEY', secrets_azure.get('api_key', '')),
            'api_version': os.getenv('AZURE_OPENAI_API_VERSION', secrets_azure.get('api_version', '2024-12-01-preview')),
            'model_name': os.getenv('AZURE_OPENAI_MODEL_NAME', secrets_azure.get('model_name', 'o3-mini-1')),
            'batch_size': int(os.getenv('DEFAULT_BATCH_SIZE', secrets_analysis.get('batch_size', 5))),
            'max_completion_tokens': int(os.getenv('DEFAULT_MAX_COMPLETION_TOKENS', secrets_analysis.get('max_completion_tokens', 10000))),
            'concurrent_workers': int(os.getenv('DEFAULT_CONCURRENT_WORKERS', secrets_analysis.get('concurrent_workers', 15)))
        }

    if SESSION_KEYS['analysis_in_progress'] not in st.session_state:
        st.session_state[SESSION_KEYS['analysis_in_progress']] = False

init_session_state()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        padding-bottom: 2rem;
    }
    .metric-card {
        background-color: #F9FAFB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E3A8A;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
    }
    .warning-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #F59E0B;
    }
    .error-box {
        background-color: #FEE2E2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #DC2626;
    }
    .info-box {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Main page content
st.markdown('<div class="main-header">📊 OMEXOM Tender Analysis </div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-driven Tender Analysis Tool</div>', unsafe_allow_html=True)
st.markdown("Powered By")
st.markdown("Business Analytics Amersfoort")
st.image("axians-1-1.webp", width=150)


# Navigation instructions
st.markdown("---")

# Welcome section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="info-box">
    <h3>👋 Welkom bij de Requirements Quality Analyzer</h3>
    <p>Deze applicatie analyseert uw requirements volgens de <b>ISO/IEC/IEEE 29148</b> standaard
    en beoordeelt ze op 8 kwaliteitscriteria:</p>
    <ul>
        <li>✅ <b>Necessary</b> - Noodzakelijk</li>
        <li>🎯 <b>Unambiguous</b> - Eenduidig</li>
        <li>📋 <b>Complete</b> - Compleet</li>
        <li>1️⃣ <b>Singular</b> - Enkelvoudig</li>
        <li>🔧 <b>Feasible</b> - Haalbaar</li>
        <li>✔️ <b>Verifiable</b> - Verifieerbaar</li>
        <li>🔗 <b>Traceable</b> - Traceerbaar</li>
        <li>🎨 <b>Implementation-free</b> - Implementatie-onafhankelijk</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# Quick start guide
st.markdown("### 🚀 Aan de slag")

steps_col1, steps_col2, steps_col3 = st.columns(3)

with steps_col1:
    st.markdown("""
    <div class="metric-card">
    <h4>1. Upload</h4>
    <p>Upload een RDF/Turtle bestand (.txt) met uw requirements</p>
    </div>
    """, unsafe_allow_html=True)

with steps_col2:
    st.markdown("""
    <div class="metric-card">
    <h4>2. Analyseer</h4>
    <p>Configureer de analyse instellingen en start de analyse</p>
    </div>
    """, unsafe_allow_html=True)

with steps_col3:
    st.markdown("""
    <div class="metric-card">
    <h4>3. Exporteer</h4>
    <p>Bekijk resultaten en exporteer naar Excel, CSV of PDF</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Current status
st.markdown("### 📍 Huidige Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    if st.session_state[SESSION_KEYS['uploaded_file']]:
        st.success("✅ Bestand geüpload")
    else:
        st.info("⏳ Wachtend op bestand")

with status_col2:
    if st.session_state[SESSION_KEYS['requirements']]:
        req_count = len(st.session_state[SESSION_KEYS['requirements']])
        st.success(f"✅ {req_count} requirements geparsed")
    else:
        st.info("⏳ Wachtend op parsing")

with status_col3:
    if st.session_state[SESSION_KEYS['analysis_results']] is not None:
        result_count = len(st.session_state[SESSION_KEYS['analysis_results']])
        st.success(f"✅ {result_count} requirements geanalyseerd")
    else:
        st.info("⏳ Wachtend op analyse")

st.markdown("---")

# Navigation
st.markdown("### 🧭 Navigatie")
st.markdown("""
Gebruik de **sidebar** aan de linkerkant om te navigeren tussen de verschillende pagina's:

- **📤 Upload** - Upload en configureer uw requirements bestand
- **⚙️ Analysis** - Start en monitor de analyse
- **📊 Dashboard** - Bekijk overzicht van resultaten
- **📋 Results** - Gedetailleerde tabel met alle requirements
- **🔍 Criteria** - Deep-dive per criterium
- **🌳 Hierarchy** - Parent-child relaties visualisatie
- **💾 Export** - Download resultaten in verschillende formaten
""")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Instellingen")

    with st.expander("🔑 Azure OpenAI Configuratie"):
        azure_endpoint = st.text_input(
            "Azure Endpoint",
            value=st.session_state[SESSION_KEYS['analyzer_config']]['azure_endpoint'],
            type="default",
            help="Azure OpenAI endpoint URL"
        )
        api_key = st.text_input(
            "API Key",
            value=st.session_state[SESSION_KEYS['analyzer_config']]['api_key'],
            type="password",
            help="Azure OpenAI API key"
        )
        model_name = st.text_input(
            "Model Name",
            value=st.session_state[SESSION_KEYS['analyzer_config']]['model_name'],
            help="Model deployment name"
        )

        if st.button("💾 Opslaan"):
            st.session_state[SESSION_KEYS['analyzer_config']]['azure_endpoint'] = azure_endpoint
            st.session_state[SESSION_KEYS['analyzer_config']]['api_key'] = api_key
            st.session_state[SESSION_KEYS['analyzer_config']]['model_name'] = model_name
            st.success("Configuratie opgeslagen!")

    with st.expander("🔧 Analyse Instellingen"):
        batch_size = st.number_input(
            "Batch Size",
            min_value=1,
            max_value=20,
            value=st.session_state[SESSION_KEYS['analyzer_config']]['batch_size'],
            help="Aantal requirements per batch"
        )
        concurrent_workers = st.number_input(
            "Concurrent Workers",
            min_value=1,
            max_value=30,
            value=st.session_state[SESSION_KEYS['analyzer_config']]['concurrent_workers'],
            help="Aantal parallelle workers"
        )
        max_tokens = st.number_input(
            "Max Completion Tokens",
            min_value=1000,
            max_value=20000,
            value=st.session_state[SESSION_KEYS['analyzer_config']]['max_completion_tokens'],
            step=1000,
            help="Maximaal aantal tokens voor response"
        )

        if st.button("💾 Update Instellingen"):
            st.session_state[SESSION_KEYS['analyzer_config']]['batch_size'] = batch_size
            st.session_state[SESSION_KEYS['analyzer_config']]['concurrent_workers'] = concurrent_workers
            st.session_state[SESSION_KEYS['analyzer_config']]['max_completion_tokens'] = max_tokens
            st.success("Instellingen bijgewerkt!")

    st.markdown("---")

    with st.expander("ℹ️ Over ISO 29148"):
        st.markdown("""
        **ISO/IEC/IEEE 29148:2018** is de internationale standaard voor:

        - Requirements engineering
        - Requirements processen
        - Requirements kwaliteit

        Deze standaard definieert best practices voor het schrijven
        en beheren van requirements in systeem- en software-engineering.
        """)

    with st.expander("❓ Help"):
        st.markdown("""
        **Veelgestelde vragen:**

        **Q: Welk bestandsformaat wordt ondersteund?**
        A: RDF/Turtle bestanden met .txt extensie

        **Q: Hoe lang duurt de analyse?**
        A: Afhankelijk van aantal requirements, ~1-3 minuten per 100 requirements

        **Q: Kan ik de resultaten opslaan?**
        A: Ja, via de Export pagina in Excel, CSV of JSON formaat
        """)

    st.markdown("---")
    st.markdown("**Versie:** 1.0.0")
    st.markdown("**Laatste update:** 2025-10-16")
