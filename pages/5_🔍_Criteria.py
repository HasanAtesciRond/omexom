"""
Criteria Deep-Dive Page
Per-criterion analysis with donut charts and failed requirements
"""

import streamlit as st
import pandas as pd
from utils.visualizations import create_donut_chart
from utils.export_utils import get_failed_requirements_for_criterion
from config.settings import SESSION_KEYS
from config.criteria_definitions import CRITERIA, CRITERIA_ORDER, get_criterion_info

st.set_page_config(page_title="Criteria Analysis", page_icon="🔍", layout="wide")

st.title("🔍 Criteria Deep-Dive")
st.markdown("Gedetailleerde analyse per ISO 29148 criterium")

# Check if analysis results exist
if st.session_state.get(SESSION_KEYS['analysis_results']) is None:
    st.warning("⚠️ Geen analyse resultaten gevonden.")
    st.stop()

df = st.session_state[SESSION_KEYS['analysis_results']]

# Criterion selection
selected_criterion = st.selectbox(
    "Selecteer een criterium",
    options=CRITERIA_ORDER,
    format_func=lambda x: f"{CRITERIA[x]['icon']} {CRITERIA[x]['name_nl']}"
)

# Get criterion info
criterion_info = get_criterion_info(selected_criterion, language='nl')

# Display criterion information
st.markdown(f"## {criterion_info['icon']} {criterion_info['name']}")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"**Beschrijving:** {criterion_info['description']}")
    st.markdown(f"**Richtlijn:** {criterion_info['guidance']}")

with col2:
    # Donut chart
    pass_count = df[selected_criterion].sum()
    fail_count = len(df) - pass_count

    fig = create_donut_chart(pass_count, fail_count, criterion_info['name'])
    st.plotly_chart(fig, width='stretch')

st.markdown("---")

# Statistics
st.markdown("### 📊 Statistieken")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Totaal Requirements", len(df))

with stat_col2:
    st.metric("Passed", pass_count, delta=f"{(pass_count/len(df)*100):.1f}%")

with stat_col3:
    st.metric("Failed", fail_count, delta=f"-{(fail_count/len(df)*100):.1f}%", delta_color="inverse")

with stat_col4:
    pass_rate = (pass_count / len(df)) * 100
    status = "✅ Goed" if pass_rate >= 80 else "⚠️ Aandacht nodig" if pass_rate >= 60 else "❌ Kritiek"
    st.metric("Status", status)

st.markdown("---")

# Failed requirements
st.markdown(f"### ❌ Gefaalde Requirements ({fail_count})")

if fail_count == 0:
    st.success(f"🎉 Alle requirements voldoen aan het '{criterion_info['name']}' criterium!")
else:
    failed_df = get_failed_requirements_for_criterion(df, selected_criterion)

    # Sort by quality score
    failed_df_sorted = failed_df.sort_values('quality_score')

    for idx, row in failed_df_sorted.iterrows():
        with st.expander(f"{row['id']} - Score: {int(row['quality_score'])}/8"):
            st.markdown(f"**Label:** {row['label']}")
            st.markdown(f"**Quality Score:** {int(row['quality_score'])}/8")

            justification_col = f"{selected_criterion}_justification"
            if justification_col in row and pd.notna(row[justification_col]):
                st.markdown("#### Waarom gefaald?")
                st.warning(row[justification_col])

            if 'suggestion' in row and pd.notna(row['suggestion']):
                st.markdown("#### 💡 Suggestie")
                st.info(row['suggestion'])

            if 'full_text' in row and pd.notna(row['full_text']):
                with st.expander("📄 Volledige tekst"):
                    st.text(row['full_text'])

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 Criteria Navigatie")

    for criterion in CRITERIA_ORDER:
        info = CRITERIA[criterion]
        if criterion == selected_criterion:
            st.markdown(f"**👉 {info['icon']} {info['name_nl']}**")
        else:
            if st.button(f"{info['icon']} {info['name_nl']}", key=f"nav_{criterion}", width='stretch'):
                st.rerun()
