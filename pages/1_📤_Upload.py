"""
Upload & Configure Page
Handles file upload, validation, and requirement parsing
"""

import streamlit as st
import os
import tempfile
from utils.rdf_parser import (
    extract_requirements_from_file,
    validate_ttl_file,
    get_requirement_statistics
)
from config.settings import SESSION_KEYS, MAX_FILE_SIZE_MB, PREVIEW_ROWS

st.set_page_config(page_title="Upload Requirements", page_icon="📤", layout="wide")

st.title("📤 Upload & Configureer")
st.markdown("Upload een RDF/Turtle bestand met requirements en bekijk de inhoud")

# Upload section
st.markdown("### 1. Upload Bestand")

uploaded_file = st.file_uploader(
    "Kies een RDF/Turtle bestand (.txt)",
    type=['txt'],
    help=f"Maximum bestandsgrootte: {MAX_FILE_SIZE_MB}MB"
)

if uploaded_file is not None:
    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"❌ Bestand is te groot ({file_size_mb:.1f}MB). Maximum: {MAX_FILE_SIZE_MB}MB")
    else:
        st.success(f"✅ Bestand geüpload: {uploaded_file.name} ({file_size_mb:.2f}MB)")

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Store in session state
        st.session_state[SESSION_KEYS['uploaded_file']] = tmp_file_path
        st.session_state[SESSION_KEYS['uploaded_filename']] = uploaded_file.name

        # Validation
        st.markdown("### 2. Validatie")

        with st.spinner("Bestand valideren..."):
            is_valid, error_msg = validate_ttl_file(tmp_file_path)

        if not is_valid:
            st.error(f"❌ Validatie mislukt: {error_msg}")
            st.info("💡 Zorg ervoor dat het bestand een geldig RDF/Turtle formaat heeft.")
        else:
            st.success("✅ Bestand is geldig RDF/Turtle formaat")

            # Parse requirements
            st.markdown("### 3. Requirements Extractie")

            if st.button("🔍 Parseer Requirements", type="primary"):
                with st.spinner("Requirements aan het extraheren..."):
                    requirements = extract_requirements_from_file(tmp_file_path)

                if not requirements:
                    st.error("❌ Geen requirements gevonden in het bestand")
                else:
                    # Store in session state
                    st.session_state[SESSION_KEYS['requirements']] = requirements

                    # Show statistics
                    stats = get_requirement_statistics(requirements)

                    st.success(f"✅ {stats['total_count']} requirements succesvol geëxtraheerd")

                    # Display statistics
                    st.markdown("### 📊 Statistieken")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Totaal Requirements", stats['total_count'])

                    with col2:
                        st.metric("Met Parent", stats['with_parent'])

                    with col3:
                        st.metric("Zonder Parent", stats['without_parent'])

                    with col4:
                        st.metric("Unieke Parents", stats['unique_parents'])

                    st.metric("Gemiddelde Tekstlengte", f"{stats['avg_text_length']} tekens")

            # Show preview if requirements are loaded
            if st.session_state[SESSION_KEYS['requirements']]:
                requirements = st.session_state[SESSION_KEYS['requirements']]
                stats = get_requirement_statistics(requirements)

                # Display statistics (always visible after parsing)
                st.markdown("### 📊 Statistieken")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Totaal Requirements", stats['total_count'])

                with col2:
                    st.metric("Met Parent", stats['with_parent'])

                with col3:
                    st.metric("Zonder Parent", stats['without_parent'])

                with col4:
                    st.metric("Unieke Parents", stats['unique_parents'])

                st.metric("Gemiddelde Tekstlengte", f"{stats['avg_text_length']} tekens")

                # Preview
                st.markdown(f"### 👀 Preview (eerste {PREVIEW_ROWS} requirements)")

                for i, req in enumerate(requirements[:PREVIEW_ROWS]):
                    with st.expander(f"{req['id']} - {req['label']}"):
                        st.markdown(f"**ID:** {req['id']}")
                        st.markdown(f"**Label:** {req['label']}")
                        st.markdown(f"**Text:** {req['text']}")
                        if req['parent_id']:
                            st.markdown(f"**Parent ID:** {req['parent_id']}")
                            st.markdown(f"**Parent Text:** {req['parent_text'][:100]}...")

                # Configuration
                st.markdown("### 4. Analyse Configuratie")

                max_reqs = st.number_input(
                    "Maximum aantal te analyseren requirements (0 = alle)",
                    min_value=0,
                    max_value=len(requirements),
                    value=0,
                    help="Beperk het aantal requirements voor testdoeleinden. 0 = analyseer alles"
                )

                # Store configuration
                if max_reqs == 0:
                    st.session_state['max_requirements_to_analyze'] = None
                else:
                    st.session_state['max_requirements_to_analyze'] = max_reqs

                # Next steps
                st.markdown("---")
                st.markdown("### ✅ Volgende Stap")

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.info("""
                    ✅ Bestand geüpload en geparsed!

                    Ga naar de **⚙️ Analysis** pagina om de analyse te starten.
                    """)

                    if st.button("➡️ Naar Analyse Pagina", type="primary", width='stretch'):
                        st.switch_page("pages/2_⚙️_Analysis.py")

else:
    # Instructions when no file is uploaded
    st.info("""
    👆 Upload een RDF/Turtle bestand om te beginnen.

    **Bestandsvereisten:**
    - Formaat: RDF/Turtle (NEN2660)
    - Extensie: .txt
    - Maximum grootte: 50MB
    - Moet requirements bevatten met `nen2660:Requirement` type

    **Voorbeeld structuur:**
    ```turtle
    @prefix nen2660: <https://w3id.org/nen2660/def#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

    <requirement/1> a nen2660:Requirement ;
        skos:notation "REQ-001" ;
        skos:prefLabel "System Requirement" ;
        rdf:value "The system shall..." .
    ```
    """)

# Sidebar info
with st.sidebar:
    st.markdown("### 📤 Upload Status")

    if st.session_state[SESSION_KEYS['uploaded_file']]:
        st.success("✅ Bestand geüpload")
    else:
        st.warning("⏳ Geen bestand geüpload")

    if st.session_state[SESSION_KEYS['requirements']]:
        req_count = len(st.session_state[SESSION_KEYS['requirements']])
        st.success(f"✅ {req_count} requirements geparsed")
    else:
        st.warning("⏳ Requirements niet geparsed")

    st.markdown("---")

    if st.button("🗑️ Reset / Nieuwe Upload"):
        st.session_state[SESSION_KEYS['uploaded_file']] = None
        st.session_state[SESSION_KEYS['uploaded_filename']] = None
        st.session_state[SESSION_KEYS['requirements']] = None
        st.session_state[SESSION_KEYS['analysis_results']] = None
        st.rerun()
