"""
Detailed Results Page
Interactive table with all requirements and filtering capabilities
"""

import streamlit as st
import pandas as pd
from utils.export_utils import filter_dataframe, get_top_worst_requirements, get_top_best_requirements
from utils.visualizations import get_quality_color
from config.settings import SESSION_KEYS
from config.criteria_definitions import CRITERIA_ORDER

st.set_page_config(page_title="Detailed Results", page_icon="📋", layout="wide")

st.title("📋 Gedetailleerde Resultaten")
st.markdown("Interactieve tabel met alle requirements en filter mogelijkheden")

# Check if analysis results exist
if st.session_state.get(SESSION_KEYS['analysis_results']) is None:
    st.warning("⚠️ Geen analyse resultaten gevonden.")
    st.stop()

df = st.session_state[SESSION_KEYS['analysis_results']]

# Filters
st.markdown("### 🔍 Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    min_score = st.number_input("Min Score", min_value=0, max_value=8, value=0)

with filter_col2:
    max_score = st.number_input("Max Score", min_value=0, max_value=8, value=8)

with filter_col3:
    search_text = st.text_input("Zoek in tekst", placeholder="Typ om te zoeken...")

with filter_col4:
    failed_criteria = st.multiselect(
        "Gefaalde criteria",
        options=CRITERIA_ORDER,
        default=[]
    )

# Apply filters
filtered_df = filter_dataframe(
    df,
    min_score=min_score,
    max_score=max_score,
    failed_criteria=failed_criteria if failed_criteria else None,
    search_text=search_text if search_text else None
)

st.markdown(f"**{len(filtered_df)} requirements** (gefilterd van {len(df)} totaal)")

# Quick view options
st.markdown("---")
view_option = st.radio(
    "Quick View",
    options=["Alle (gefilterd)", "Top 10 Beste", "Top 10 Slechtste"],
    horizontal=True
)

if view_option == "Top 10 Beste":
    display_df = get_top_best_requirements(filtered_df, n=10)
    st.info("📊 Top 10 requirements met hoogste quality scores")
elif view_option == "Top 10 Slechtste":
    display_df = get_top_worst_requirements(filtered_df, n=10)
    st.warning("⚠️ Top 10 requirements met laagste quality scores")
else:
    display_df = filtered_df

# Display table
st.markdown("### 📊 Requirements Tabel")

for idx, row in display_df.iterrows():
    quality_score = int(row['quality_score'])
    color = get_quality_color(quality_score)

    with st.expander(f"{row['id']} | Score: {quality_score}/8", expanded=False):
        # Header
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**Label:** {row['label']}")
            st.markdown(f"**ID:** {row['id']}")
            if row.get('parent_id'):
                st.markdown(f"**Parent ID:** {row['parent_id']}")

        with col2:
            st.markdown(
                f'<div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">'
                f'<div style="font-size:32px; font-weight:bold; color:white;">{quality_score}</div>'
                f'<div style="color:white;">/ 8</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Criteria checkboxes
        st.markdown("#### Criteria Status")

        criteria_cols = st.columns(4)
        criteria_names = {
            'necessary': '✅ Necessary',
            'unambiguous': '🎯 Unambiguous',
            'complete': '📋 Complete',
            'singular': '1️⃣ Singular',
            'feasible': '🔧 Feasible',
            'verifiable': '✔️ Verifiable',
            'traceable': '🔗 Traceable',
            'implementation_free': '🎨 Impl-Free'
        }

        for idx_crit, criterion in enumerate(CRITERIA_ORDER):
            with criteria_cols[idx_crit % 4]:
                status = row.get(criterion, False)
                status_icon = "✅" if status else "❌"
                status_text = "Pass" if status else "Fail"
                st.markdown(f"{status_icon} **{criteria_names[criterion]}**: {status_text}")

        # Justifications
        st.markdown("#### Justifications")

        for criterion in CRITERIA_ORDER:
            justification_key = f"{criterion}_justification"
            if justification_key in row and pd.notna(row[justification_key]):
                status = row.get(criterion, False)
                if not status:  # Only show failed criteria justifications by default
                    with st.expander(f"❌ {criteria_names[criterion]} - Justification"):
                        st.markdown(row[justification_key])

        # Show all justifications button
        if st.checkbox(f"Toon alle justifications voor {row['id']}", key=f"show_all_{idx}"):
            for criterion in CRITERIA_ORDER:
                justification_key = f"{criterion}_justification"
                if justification_key in row and pd.notna(row[justification_key]):
                    status = row.get(criterion, False)
                    status_icon = "✅" if status else "❌"
                    st.markdown(f"**{status_icon} {criteria_names[criterion]}:**")
                    st.markdown(row[justification_key])
                    st.markdown("---")

        # Suggestion
        if 'suggestion' in row and pd.notna(row['suggestion']):
            st.markdown("#### 💡 Verbeter Suggestie")
            st.info(row['suggestion'])

        # Full text
        with st.expander("📄 Volledige Requirement Tekst"):
            st.text(row.get('full_text', 'N/A'))

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Resultaten Info")
    st.metric("Totaal Requirements", len(df))
    st.metric("Gefilterde Requirements", len(filtered_df))
    st.metric("Weergegeven", len(display_df))

    st.markdown("---")

    if st.button("📊 Naar Dashboard"):
        st.switch_page("pages/3_📊_Dashboard.py")

    if st.button("💾 Exporteer Gefilterde Resultaten"):
        st.info("Ga naar de Export pagina voor export opties")
