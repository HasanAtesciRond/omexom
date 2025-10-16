"""
Visualization utilities for ISO 29148 Requirements Analysis
Creates interactive charts using Plotly
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List


def create_quality_score_histogram(df: pd.DataFrame) -> go.Figure:
    """
    Creates a histogram showing the distribution of quality scores.

    Args:
        df: DataFrame with 'quality_score' column

    Returns:
        Plotly figure object
    """
    # Count occurrences of each score
    score_counts = df['quality_score'].value_counts().sort_index()

    # Create color mapping (Red -> Orange -> Yellow -> Green)
    colors = []
    for score in score_counts.index:
        if score <= 2:
            colors.append('#DC2626')  # Red
        elif score <= 4:
            colors.append('#F59E0B')  # Orange/Amber
        elif score <= 6:
            colors.append('#FCD34D')  # Yellow
        else:
            colors.append('#10B981')  # Green

    fig = go.Figure(data=[
        go.Bar(
            x=score_counts.index,
            y=score_counts.values,
            marker_color=colors,
            text=score_counts.values,
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Quality Score Distribution",
        xaxis_title="Quality Score (0-8)",
        yaxis_title="Number of Requirements",
        showlegend=False,
        height=400,
        template="plotly_white"
    )

    return fig


def create_criteria_pass_rate_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates a horizontal bar chart showing pass rates for each criterion.

    Args:
        df: DataFrame with boolean columns for each criterion

    Returns:
        Plotly figure object
    """
    criteria = [
        'necessary', 'unambiguous', 'complete', 'singular',
        'feasible', 'verifiable', 'traceable', 'implementation_free'
    ]

    criteria_labels = {
        'necessary': 'Necessary (Noodzakelijk)',
        'unambiguous': 'Unambiguous (Eenduidig)',
        'complete': 'Complete (Compleet)',
        'singular': 'Singular (Enkelvoudig)',
        'feasible': 'Feasible (Haalbaar)',
        'verifiable': 'Verifiable (Verifieerbaar)',
        'traceable': 'Traceable (Traceerbaar)',
        'implementation_free': 'Implementation-free (Impl-onafh.)'
    }

    pass_rates = []
    for criterion in criteria:
        if criterion in df.columns:
            pass_rate = (df[criterion].sum() / len(df)) * 100
            pass_rates.append(pass_rate)
        else:
            pass_rates.append(0)

    # Color code: Green if >80%, Yellow if 60-80%, Red if <60%
    colors = ['#10B981' if rate >= 80 else '#FCD34D' if rate >= 60 else '#DC2626' for rate in pass_rates]

    labels = [criteria_labels.get(c, c) for c in criteria]

    fig = go.Figure(data=[
        go.Bar(
            y=labels,
            x=pass_rates,
            orientation='h',
            marker_color=colors,
            text=[f"{rate:.1f}%" for rate in pass_rates],
            textposition='auto',
        )
    ])

    # Add 80% threshold line
    fig.add_vline(x=80, line_dash="dash", line_color="gray", annotation_text="80% target")

    fig.update_layout(
        title="ISO 29148 Criteria Pass Rates",
        xaxis_title="Pass Rate (%)",
        yaxis_title="",
        showlegend=False,
        height=500,
        template="plotly_white"
    )

    return fig


def create_parent_quality_treemap(df: pd.DataFrame, all_requirements: List[Dict]) -> go.Figure:
    """
    Creates a treemap showing parent requirements colored by average quality score.

    Args:
        df: Analysis DataFrame with parent_id and quality_score
        all_requirements: Original requirements list for parent text lookup

    Returns:
        Plotly figure object
    """
    # Filter for requirements with parents
    children_df = df[df['parent_id'].notna()].copy()

    if children_df.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No parent-child relationships found",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Calculate parent statistics
    parent_stats = children_df.groupby('parent_id').agg(
        count=('id', 'count'),
        avg_score=('quality_score', 'mean')
    ).reset_index()

    # Get parent text
    parent_text_map = {req['id']: req['text'][:50] + '...' for req in all_requirements}
    parent_stats['parent_text'] = parent_stats['parent_id'].map(parent_text_map)

    # Create labels
    parent_stats['label'] = parent_stats['parent_id'] + '<br>' + parent_stats['count'].astype(str) + ' children'

    fig = go.Figure(go.Treemap(
        labels=parent_stats['label'],
        parents=[""] * len(parent_stats),
        values=parent_stats['count'],
        marker=dict(
            colorscale='RdYlGn',
            cmid=4,
            cmin=0,
            cmax=8,
            colorbar=dict(title="Avg Quality Score"),
            line=dict(width=2)
        ),
        marker_colorscale='RdYlGn',
        customdata=parent_stats[['avg_score', 'parent_text']],
        hovertemplate='<b>%{label}</b><br>Avg Score: %{customdata[0]:.1f}<br>%{customdata[1]}<extra></extra>',
        text=parent_stats['avg_score'].round(1),
        textposition='middle center'
    ))

    fig.update_layout(
        title="Parent Requirements Quality Heatmap",
        height=500,
    )

    return fig


def create_failure_heatmap(df: pd.DataFrame, top_n: int = 50) -> go.Figure:
    """
    Creates a heatmap showing which criteria failed for the worst requirements.

    Args:
        df: Analysis DataFrame
        top_n: Number of worst requirements to show

    Returns:
        Plotly figure object
    """
    # Get top N worst requirements
    worst_reqs = df.nsmallest(min(top_n, len(df)), 'quality_score')

    criteria = [
        'necessary', 'unambiguous', 'complete', 'singular',
        'feasible', 'verifiable', 'traceable', 'implementation_free'
    ]

    # Create matrix (1 for pass, 0 for fail)
    matrix_data = []
    for criterion in criteria:
        if criterion in worst_reqs.columns:
            matrix_data.append(worst_reqs[criterion].astype(int).tolist())
        else:
            matrix_data.append([0] * len(worst_reqs))

    criteria_labels = ['Necessary', 'Unambiguous', 'Complete', 'Singular',
                      'Feasible', 'Verifiable', 'Traceable', 'Impl-Free']

    fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=worst_reqs['id'].tolist(),
        y=criteria_labels,
        colorscale=[[0, '#DC2626'], [1, '#10B981']],
        showscale=False,
        hovertemplate='Req: %{x}<br>Criterion: %{y}<br>Status: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title=f"Failure Matrix - Top {len(worst_reqs)} Worst Requirements",
        xaxis_title="Requirement ID",
        yaxis_title="ISO 29148 Criteria",
        height=400,
        template="plotly_white"
    )

    return fig


def create_donut_chart(pass_count: int, fail_count: int, criterion_name: str) -> go.Figure:
    """
    Creates a donut chart for pass/fail ratio of a single criterion.

    Args:
        pass_count: Number of requirements that passed
        fail_count: Number of requirements that failed
        criterion_name: Name of the criterion

    Returns:
        Plotly figure object
    """
    labels = ['Pass', 'Fail']
    values = [pass_count, fail_count]
    colors = ['#10B981', '#DC2626']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='auto'
    )])

    total = pass_count + fail_count
    pass_rate = (pass_count / total * 100) if total > 0 else 0

    fig.update_layout(
        title=f"{criterion_name}<br>Pass Rate: {pass_rate:.1f}%",
        showlegend=True,
        height=300,
        template="plotly_white"
    )

    return fig


def create_hierarchy_tree(df: pd.DataFrame, all_requirements: List[Dict]) -> go.Figure:
    """
    Creates an interactive tree diagram showing parent-child relationships.

    Args:
        df: Analysis DataFrame
        all_requirements: Original requirements list

    Returns:
        Plotly figure object
    """
    # Build parent-child relationships
    parents = []
    children = []
    scores = []
    labels = []

    # Add root
    root_reqs = [req for req in all_requirements if req.get('parent_id') is None]

    for req in all_requirements:
        req_id = req['id']
        parent_id = req.get('parent_id', '')

        if parent_id:
            parents.append(parent_id)
            children.append(req_id)
        else:
            parents.append('')
            children.append(req_id)

        # Get quality score from analysis
        score_row = df[df['id'] == req_id]
        score = score_row['quality_score'].values[0] if not score_row.empty else 0
        scores.append(score)
        labels.append(f"{req_id}<br>Score: {score}")

    # Color mapping
    colors = []
    for score in scores:
        if score >= 7:
            colors.append('#10B981')  # Green
        elif score >= 5:
            colors.append('#FCD34D')  # Yellow
        elif score >= 3:
            colors.append('#F59E0B')  # Orange
        else:
            colors.append('#DC2626')  # Red

    fig = go.Figure(go.Sunburst(
        ids=children,
        labels=labels,
        parents=parents,
        marker=dict(colors=colors),
        branchvalues="total"
    ))

    fig.update_layout(
        title="Requirements Hierarchy Tree",
        height=600,
    )

    return fig


def get_quality_color(score: int) -> str:
    """
    Returns color code based on quality score.

    Args:
        score: Quality score (0-8)

    Returns:
        Hex color code
    """
    if score >= 7:
        return '#10B981'  # Green
    elif score >= 5:
        return '#FCD34D'  # Yellow
    elif score >= 3:
        return '#F59E0B'  # Orange
    else:
        return '#DC2626'  # Red
