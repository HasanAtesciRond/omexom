"""
Parent-Child Hierarchy Page
Visualizes parent-child relationships and aggregated quality metrics
"""

import streamlit as st
import pandas as pd
from utils.visualizations import create_hierarchy_tree
from config.settings import SESSION_KEYS, COLORS

st.set_page_config(page_title="Hierarchy View", page_icon="🌳", layout="wide")

st.title("🌳 Parent-Child Hiërarchie")
st.markdown("Visualisatie van parent-child relaties en quality metrics")

# Check if analysis results exist
if st.session_state.get(SESSION_KEYS['analysis_results']) is None:
    st.warning("⚠️ Geen analyse resultaten gevonden.")
    st.stop()

df = st.session_state[SESSION_KEYS['analysis_results']]
requirements = st.session_state.get(SESSION_KEYS['requirements'], [])

# Check if there are parent-child relationships
children_df = df[df['parent_id'].notna()]

if children_df.empty:
    st.info("ℹ️ Er zijn geen parent-child relaties gevonden in de data.")
    st.stop()

# Statistics
st.markdown("### 📊 Hiërarchie Statistieken")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    total_parents = df['parent_id'].nunique()
    st.metric("Unieke Parents", total_parents)

with stat_col2:
    total_children = len(children_df)
    st.metric("Requirements met Parent", total_children)

with stat_col3:
    orphans = len(df[df['parent_id'].isna()])
    st.metric("Requirements zonder Parent", orphans)

with stat_col4:
    avg_children = total_children / total_parents if total_parents > 0 else 0
    st.metric("Gem. Children per Parent", f"{avg_children:.1f}")

st.markdown("---")

# Hierarchy Tree Visualization
st.markdown("### 🌲 Hiërarchie Boom")
st.info("💡 Tip: Klik op segmenten om in/uit te zoomen")

fig_tree = create_hierarchy_tree(df, requirements)
st.plotly_chart(fig_tree, use_container_width=True)

st.markdown("---")

# Parent Summary Table
st.markdown("### 📋 Parent Summary Tabel")

# Calculate parent statistics
parent_stats = children_df.groupby('parent_id').agg(
    child_count=('id', 'count'),
    avg_quality_score=('quality_score', 'mean'),
    min_quality_score=('quality_score', 'min'),
    max_quality_score=('quality_score', 'max'),
    child_ids=('id', lambda x: ', '.join(x))
).reset_index()

# Get parent text
parent_text_map = {req['id']: req['text'] for req in requirements}
parent_stats['parent_text'] = parent_stats['parent_id'].apply(
    lambda x: parent_text_map.get(x, 'N/A')[:100] + '...' if parent_text_map.get(x) else 'N/A'
)

# Sort by average quality score
parent_stats_sorted = parent_stats.sort_values('avg_quality_score')

# Display each parent
for idx, row in parent_stats_sorted.iterrows():
    avg_score = row['avg_quality_score']

    # Color based on average score
    if avg_score >= 7:
        color = COLORS['success']
    elif avg_score >= 5:
        color = COLORS['warning']
    elif avg_score >= 3:
        color = COLORS['accent']
    else:
        color = COLORS['danger']

    with st.expander(f"{row['parent_id']} - Avg Score: {avg_score:.2f}/8 ({row['child_count']} children)"):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**Parent ID:** {row['parent_id']}")
            st.markdown(f"**Parent Text:** {row['parent_text']}")
            st.markdown(f"**Child IDs:** {row['child_ids']}")

        with col2:
            st.markdown(
                f'<div style="background-color:{color}; padding:15px; border-radius:8px; text-align:center;">'
                f'<div style="font-size:24px; font-weight:bold; color:white;">{avg_score:.2f}</div>'
                f'<div style="color:white;">Avg Score</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Statistics for this parent
        stats_col1, stats_col2, stats_col3 = st.columns(3)

        with stats_col1:
            st.metric("Aantal Children", row['child_count'])

        with stats_col2:
            st.metric("Min Score", f"{row['min_quality_score']}/8")

        with stats_col3:
            st.metric("Max Score", f"{row['max_quality_score']}/8")

        # Show children
        st.markdown("#### Children Requirements")

        child_ids = row['child_ids'].split(', ')
        children_for_parent = df[df['id'].isin(child_ids)]

        for _, child_row in children_for_parent.iterrows():
            child_score = int(child_row['quality_score'])
            child_color = COLORS['success'] if child_score >= 7 else COLORS['warning'] if child_score >= 5 else COLORS['accent'] if child_score >= 3 else COLORS['danger']

            st.markdown(
                f'<div style="background-color:{child_color}20; padding:8px; margin:4px; border-radius:4px; border-left:4px solid {child_color}">'
                f'<b>{child_row["id"]}</b> - Score: {child_score}/8 | {child_row["label"]}'
                f'</div>',
                unsafe_allow_html=True
            )

# Sidebar
with st.sidebar:
    st.markdown("### 🌳 Hiërarchie Info")

    st.metric("Totaal Parents", total_parents)
    st.metric("Totaal Children", total_children)
    st.metric("Orphans", orphans)

    st.markdown("---")

    # Best and worst parents
    if not parent_stats.empty:
        best_parent = parent_stats.loc[parent_stats['avg_quality_score'].idxmax()]
        worst_parent = parent_stats.loc[parent_stats['avg_quality_score'].idxmin()]

        st.markdown("#### 🏆 Beste Parent")
        st.success(f"{best_parent['parent_id']}\n\nScore: {best_parent['avg_quality_score']:.2f}")

        st.markdown("#### ⚠️ Slechtste Parent")
        st.error(f"{worst_parent['parent_id']}\n\nScore: {worst_parent['avg_quality_score']:.2f}")
