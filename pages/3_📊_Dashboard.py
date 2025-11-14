"""
Dashboard Overview Page
Shows key metrics and visualizations of analysis results
"""

import streamlit as st
import pandas as pd
from utils.visualizations import (
    create_quality_score_histogram,
    create_criteria_pass_rate_chart,
    create_parent_quality_treemap,
    create_failure_heatmap
)
from utils.export_utils import create_summary_statistics
from config.settings import SESSION_KEYS, COLORS

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard Overzicht")
st.markdown("Belangrijkste metrics en visualisaties van de analyse resultaten")

# Check if analysis results exist
if st.session_state.get(SESSION_KEYS['analysis_results']) is None:
    st.warning("⚠️ Geen analyse resultaten gevonden. Voer eerst een analyse uit.")
    if st.button("➡️ Naar Analyse Pagina"):
        st.switch_page("pages/2_⚙️_Analysis.py")
    st.stop()

df = st.session_state[SESSION_KEYS['analysis_results']]
requirements = st.session_state.get(SESSION_KEYS['requirements'], [])

# Calculate statistics
stats = create_summary_statistics(df)

# Top KPIs
st.markdown("### 🎯 Belangrijkste Metrics")

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.metric(
        "Totaal Requirements",
        stats['total_requirements']
    )

with kpi_col2:
    avg_score = stats['average_quality_score']
    score_color = COLORS['success'] if avg_score >= 6 else COLORS['warning'] if avg_score >= 4 else COLORS['danger']
    st.metric(
        "Gemiddelde Score",
        f"{avg_score:.2f}/8"
    )

with kpi_col3:
    excellent_pct = (stats.get('excellent_count', 0) / stats['total_requirements']) * 100
    st.metric(
        "Excellent (7-8)",
        f"{stats.get('excellent_count', 0)}",
        delta=f"{excellent_pct:.1f}%"
    )

with kpi_col4:
    poor_pct = (stats.get('poor_count', 0) / stats['total_requirements']) * 100
    st.metric(
        "Poor (0-2)",
        f"{stats.get('poor_count', 0)}",
        delta=f"-{poor_pct:.1f}%" if poor_pct > 0 else "0%",
        delta_color="inverse"
    )

with kpi_col5:
    median_score = stats['median_quality_score']
    st.metric(
        "Mediaan Score",
        f"{median_score:.1f}/8"
    )

st.markdown("---")

# Quality Distribution
st.markdown("### 📈 Quality Score Distributie")

col1, col2 = st.columns([2, 1])

with col1:
    fig_histogram = create_quality_score_histogram(df)
    st.plotly_chart(fig_histogram, width='stretch')

with col2:
    st.markdown("#### Score Verdeling")
    score_dist = stats.get('score_distribution', {})

    for score in range(8, -1, -1):
        count = score_dist.get(score, 0)
        pct = (count / stats['total_requirements']) * 100 if stats['total_requirements'] > 0 else 0

        if score >= 7:
            color = COLORS['success']
        elif score >= 5:
            color = COLORS['warning']
        elif score >= 3:
            color = COLORS['accent']
        else:
            color = COLORS['danger']

        st.markdown(
            f'<div style="background-color:{color}20; padding:8px; margin:4px; border-radius:4px; border-left:4px solid {color}">'
            f'Score {score}: <b>{count}</b> ({pct:.1f}%)'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# Criteria Pass Rates
st.markdown("### ✅ ISO 29148 Criteria Pass Rates")

fig_criteria = create_criteria_pass_rate_chart(df)
st.plotly_chart(fig_criteria, width='stretch')

# Criteria details
st.markdown("#### Criteria Details")

criteria_cols = st.columns(4)

criteria_data = [
    ('necessary', 'Necessary', '✅'),
    ('unambiguous', 'Unambiguous', '🎯'),
    ('complete', 'Complete', '📋'),
    ('singular', 'Singular', '1️⃣'),
    ('feasible', 'Feasible', '🔧'),
    ('verifiable', 'Verifiable', '✔️'),
    ('traceable', 'Traceable', '🔗'),
    ('implementation_free', 'Impl-Free', '🎨')
]

for idx, (key, name, icon) in enumerate(criteria_data):
    with criteria_cols[idx % 4]:
        pass_rate = stats.get(f'{key}_pass_rate', 0)
        pass_count = stats.get(f'{key}_pass_count', 0)
        fail_count = stats.get(f'{key}_fail_count', 0)

        color = COLORS['success'] if pass_rate >= 80 else COLORS['warning'] if pass_rate >= 60 else COLORS['danger']

        st.markdown(
            f'<div style="background-color:{color}20; padding:12px; margin:8px; border-radius:8px; border-left:4px solid {color}">'
            f'<div style="font-size:24px;">{icon}</div>'
            f'<div style="font-weight:bold; margin-top:8px;">{name}</div>'
            f'<div style="font-size:20px; color:{color}; font-weight:bold;">{pass_rate:.1f}%</div>'
            f'<div style="font-size:12px; color:#6B7280;">✓ {pass_count} | ✗ {fail_count}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# Parent-Child Quality Heatmap
if requirements and df[df['parent_id'].notna()].shape[0] > 0:
    st.markdown("### 🌳 Parent-Child Quality Heatmap")
    fig_treemap = create_parent_quality_treemap(df, requirements)
    st.plotly_chart(fig_treemap, width='stretch')
else:
    st.info("ℹ️ Geen parent-child relaties gevonden in de data")

st.markdown("---")

# Failure Matrix
st.markdown("### 🔥 Failure Matrix - Slechtste Requirements")

top_n = st.slider("Aantal slechtste requirements", min_value=10, max_value=100, value=50, step=10)
fig_heatmap = create_failure_heatmap(df, top_n=top_n)
st.plotly_chart(fig_heatmap, width='stretch')

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard Filters")

    st.info("Filter opties komen in een latere versie")

    st.markdown("---")
    st.markdown("### 🔍 Quick Actions")

    if st.button("📋 Naar Resultaten", width='stretch'):
        st.switch_page("pages/4_📋_Results.py")

    if st.button("💾 Naar Export", width='stretch'):
        st.switch_page("pages/7_💾_Export.py")
