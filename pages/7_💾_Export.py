"""
Export Page
Download analysis results in various formats (Excel, CSV, JSON)
"""

import streamlit as st
import os
from datetime import datetime
from utils.export_utils import (
    create_excel_export,
    create_csv_export,
    create_json_export,
    create_summary_statistics,
    filter_dataframe
)
from config.settings import SESSION_KEYS
from config.criteria_definitions import CRITERIA_ORDER

st.set_page_config(page_title="Export Results", page_icon="💾", layout="wide")

st.title("💾 Exporteer Resultaten")
st.markdown("Download analyse resultaten in verschillende formaten")

# Check if analysis results exist
if st.session_state.get(SESSION_KEYS['analysis_results']) is None:
    st.warning("⚠️ Geen analyse resultaten gevonden om te exporteren.")
    if st.button("➡️ Naar Analyse Pagina"):
        st.switch_page("pages/2_⚙️_Analysis.py")
    st.stop()

df = st.session_state[SESSION_KEYS['analysis_results']]
requirements = st.session_state.get(SESSION_KEYS['requirements'], [])

# Export options
st.markdown("### 📋 Export Opties")

export_col1, export_col2 = st.columns([1, 2])

with export_col1:
    st.markdown("#### Formaat Selectie")

    export_format = st.radio(
        "Kies een formaat",
        options=["Excel (.xlsx)", "CSV", "JSON"],
        help="Selecteer het gewenste export formaat"
    )

    st.markdown("#### Filters (optioneel)")

    apply_filters = st.checkbox("Filters toepassen", value=False)

    if apply_filters:
        min_score = st.number_input("Min Score", 0, 8, 0)
        max_score = st.number_input("Max Score", 0, 8, 8)
        search_text = st.text_input("Zoek tekst")
        failed_criteria = st.multiselect("Gefaalde criteria", CRITERIA_ORDER)

        # Apply filters
        filtered_df = filter_dataframe(
            df,
            min_score=min_score,
            max_score=max_score,
            failed_criteria=failed_criteria if failed_criteria else None,
            search_text=search_text if search_text else None
        )
    else:
        filtered_df = df

    st.info(f"📊 {len(filtered_df)} requirements zullen worden geëxporteerd")

with export_col2:
    st.markdown("#### Preview & Statistieken")

    stats = create_summary_statistics(filtered_df)

    # Summary metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Totaal Requirements", stats['total_requirements'])

    with metric_col2:
        st.metric("Gemiddelde Score", f"{stats['average_quality_score']:.2f}/8")

    with metric_col3:
        st.metric("Mediaan Score", f"{stats['median_quality_score']:.1f}/8")

    # Quality distribution
    st.markdown("##### Quality Verdeling")

    dist_col1, dist_col2, dist_col3, dist_col4 = st.columns(4)

    with dist_col1:
        st.metric("Excellent (7-8)", stats.get('excellent_count', 0))

    with dist_col2:
        st.metric("Good (5-6)", stats.get('good_count', 0))

    with dist_col3:
        st.metric("Fair (3-4)", stats.get('fair_count', 0))

    with dist_col4:
        st.metric("Poor (0-2)", stats.get('poor_count', 0))

    # Preview table
    st.markdown("##### Preview (eerste 5 rijen)")
    preview_cols = ['id', 'label', 'quality_score', 'necessary', 'unambiguous', 'complete', 'singular']
    preview_cols = [col for col in preview_cols if col in filtered_df.columns]
    st.dataframe(filtered_df[preview_cols].head(), width='stretch')

st.markdown("---")

# Filename configuration
st.markdown("### 📝 Bestandsnaam Configuratie")

# Get original filename from session state - always use as default base name
original_filename = st.session_state.get(SESSION_KEYS['uploaded_filename'])
if original_filename:
    # Remove extension (.txt or .ttl) - this is the default base name
    base_name = os.path.splitext(original_filename)[0]
    st.info(f"📁 Standaard basisnaam: `{base_name}` (van geüpload bestand `{original_filename}`)")
else:
    # If no filename found, show warning but still allow export with a default
    st.warning("⚠️ Geen originele bestandsnaam gevonden. Upload het bestand opnieuw voor de juiste bestandsnaam.")
    base_name = 'ISO29148_Analysis'

# Generate timestamp for filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Show preview of default filename
default_filename_example = f"{base_name}_powerbid_{timestamp}"
st.caption(f"💡 Standaard bestandsnaam: `{default_filename_example}.{{extensie}}`")

# Custom filename input - overrides the default if provided
custom_filename = st.text_input(
    "Aangepaste bestandsnaam (optioneel)",
    value="",
    help="Laat leeg om automatische naam te gebruiken (`{basisnaam}_powerbid_{{timestamp}}.{{ext}}`). Extensie wordt automatisch toegevoegd.",
    placeholder="Laat leeg voor automatische naam"
)

# Export buttons
st.markdown("### 📥 Download")

col1, col2, col3 = st.columns(3)

with col1:
    if export_format == "Excel (.xlsx)" or st.button("📊 Download Excel", width='stretch', type="primary" if export_format == "Excel (.xlsx)" else "secondary"):
        with st.spinner("Excel bestand genereren..."):
            excel_data = create_excel_export(filtered_df, requirements)

        # Generate filename
        if custom_filename and custom_filename.strip():
            filename = custom_filename.strip()
            if not filename.endswith('.xlsx'):
                filename = f"{filename}.xlsx"
        else:
            filename = f"{base_name}_powerbid_{timestamp}.xlsx"

        st.download_button(
            label="⬇️ Download Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )
        st.success("✅ Excel bestand klaar voor download")

with col2:
    if export_format == "CSV" or st.button("📄 Download CSV", width='stretch', type="primary" if export_format == "CSV" else "secondary"):
        include_justifications = st.checkbox("Inclusief justifications", value=True, key="csv_just")

        with st.spinner("CSV bestand genereren..."):
            csv_data = create_csv_export(filtered_df, include_justifications=include_justifications)

        # Generate filename
        if custom_filename and custom_filename.strip():
            filename = custom_filename.strip()
            if not filename.endswith('.csv'):
                filename = f"{filename}.csv"
        else:
            filename = f"{base_name}_powerbid_{timestamp}.csv"

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=filename,
            mime="text/csv",
            width='stretch'
        )
        st.success("✅ CSV bestand klaar voor download")

with col3:
    if export_format == "JSON" or st.button("🔧 Download JSON", width='stretch', type="primary" if export_format == "JSON" else "secondary"):
        with st.spinner("JSON bestand genereren..."):
            json_data = create_json_export(filtered_df)

        # Generate filename
        if custom_filename and custom_filename.strip():
            filename = custom_filename.strip()
            if not filename.endswith('.json'):
                filename = f"{filename}.json"
        else:
            filename = f"{base_name}_powerbid_{timestamp}.json"

        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name=filename,
            mime="application/json",
            width='stretch'
        )
        st.success("✅ JSON bestand klaar voor download")

st.markdown("---")

# Export information
st.markdown("### ℹ️ Export Informatie")

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    **Excel (.xlsx)**
    - 2 sheets: Detailed Analysis + Parent Summary
    - Inclusief alle criteria en justifications
    - Beste voor rapportage en analyse
    - Compatibel met Microsoft Excel
    """)

with info_col2:
    st.markdown("""
    **CSV**
    - Platte tabel structuur
    - Optioneel zonder justifications
    - Beste voor data processing
    - Compatibel met alle tools
    """)

with info_col3:
    st.markdown("""
    **JSON**
    - Gestructureerd data formaat
    - Inclusief alle nested data
    - Beste voor API integratie
    - Programmeerbaar gebruik
    """)

# Sidebar
with st.sidebar:
    st.markdown("### 💾 Export Status")

    st.metric("Te exporteren", len(filtered_df))

    if apply_filters:
        st.info("Filters actief")
    else:
        st.success("Geen filters")

    st.markdown("---")
    st.markdown("### 🔗 Quick Links")

    if st.button("📊 Naar Dashboard", width='stretch'):
        st.switch_page("pages/3_📊_Dashboard.py")

    if st.button("📋 Naar Resultaten", width='stretch'):
        st.switch_page("pages/4_📋_Results.py")
