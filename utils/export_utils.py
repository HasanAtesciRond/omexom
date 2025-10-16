"""
Export utilities for ISO 29148 Requirements Analysis
Handles Excel, CSV, JSON, and PDF exports
"""

import pandas as pd
import io
from typing import List, Dict


def create_excel_export(df: pd.DataFrame, all_requirements: List[Dict]) -> bytes:
    """
    Creates an Excel file with two sheets: detailed analysis and parent summary.

    Args:
        df: Analysis results DataFrame
        all_requirements: Original requirements list for parent lookup

    Returns:
        Bytes object containing the Excel file
    """
    output = io.BytesIO()

    # Prepare detailed sheet
    detailed_df = df.copy()
    ordered_columns = [
        'id', 'label', 'quality_score', 'parent_id', 'source',
        'necessary', 'necessary_justification',
        'unambiguous', 'unambiguous_justification',
        'complete', 'complete_justification',
        'singular', 'singular_justification',
        'feasible', 'feasible_justification',
        'verifiable', 'verifiable_justification',
        'traceable', 'traceable_justification',
        'implementation_free', 'implementation_free_justification',
        'suggestion', 'full_text'
    ]

    # Ensure all columns exist
    for col in ordered_columns:
        if col not in detailed_df.columns:
            detailed_df[col] = None

    detailed_df = detailed_df[ordered_columns]

    # Create parent summary
    children_df = detailed_df[detailed_df['parent_id'].notna()].copy()
    children_df['quality_score'] = pd.to_numeric(children_df['quality_score'], errors='coerce')

    if not children_df.empty:
        summary = children_df.groupby('parent_id').agg(
            child_req_ids=('id', lambda x: ', '.join(x)),
            number_of_children=('id', 'count'),
            average_quality_score=('quality_score', 'mean')
        ).reset_index()

        # Get parent text
        parent_info = {req['id']: req['text'] for req in all_requirements}
        summary['parent_text'] = summary['parent_id'].map(parent_info)

        summary = summary[['parent_id', 'parent_text', 'number_of_children',
                          'average_quality_score', 'child_req_ids']]
    else:
        summary = pd.DataFrame(columns=['parent_id', 'parent_text', 'number_of_children',
                                       'average_quality_score', 'child_req_ids'])

    # Write to Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        detailed_df.to_excel(writer, sheet_name='ISO 29148 Analysis', index=False)
        summary.to_excel(writer, sheet_name='Parent Summary', index=False)

    output.seek(0)
    return output.getvalue()


def create_csv_export(df: pd.DataFrame, include_justifications: bool = True) -> bytes:
    """
    Creates a CSV export of the analysis results.

    Args:
        df: Analysis results DataFrame
        include_justifications: Whether to include justification columns

    Returns:
        Bytes object containing the CSV file
    """
    export_df = df.copy()

    if not include_justifications:
        # Remove justification columns
        justification_cols = [col for col in export_df.columns if '_justification' in col]
        export_df = export_df.drop(columns=justification_cols)

    output = io.StringIO()
    export_df.to_csv(output, index=False)
    return output.getvalue().encode('utf-8')


def create_json_export(df: pd.DataFrame) -> bytes:
    """
    Creates a JSON export of the analysis results.

    Args:
        df: Analysis results DataFrame

    Returns:
        Bytes object containing the JSON file
    """
    json_str = df.to_json(orient='records', indent=2, force_ascii=False)
    return json_str.encode('utf-8')


def create_summary_statistics(df: pd.DataFrame) -> Dict:
    """
    Creates summary statistics for the analysis results.

    Args:
        df: Analysis results DataFrame

    Returns:
        Dictionary with summary statistics
    """
    criteria = [
        'necessary', 'unambiguous', 'complete', 'singular',
        'feasible', 'verifiable', 'traceable', 'implementation_free'
    ]

    stats = {
        'total_requirements': len(df),
        'average_quality_score': df['quality_score'].mean() if 'quality_score' in df.columns else 0,
        'median_quality_score': df['quality_score'].median() if 'quality_score' in df.columns else 0,
        'min_quality_score': df['quality_score'].min() if 'quality_score' in df.columns else 0,
        'max_quality_score': df['quality_score'].max() if 'quality_score' in df.columns else 0,
    }

    # Calculate pass rates per criterion
    for criterion in criteria:
        if criterion in df.columns:
            pass_count = df[criterion].sum()
            pass_rate = (pass_count / len(df)) * 100
            stats[f'{criterion}_pass_rate'] = pass_rate
            stats[f'{criterion}_pass_count'] = pass_count
            stats[f'{criterion}_fail_count'] = len(df) - pass_count

    # Score distribution
    if 'quality_score' in df.columns:
        stats['score_distribution'] = df['quality_score'].value_counts().sort_index().to_dict()

    # Requirements by quality category
    if 'quality_score' in df.columns:
        stats['excellent_count'] = len(df[df['quality_score'] >= 7])  # 7-8
        stats['good_count'] = len(df[(df['quality_score'] >= 5) & (df['quality_score'] < 7)])  # 5-6
        stats['fair_count'] = len(df[(df['quality_score'] >= 3) & (df['quality_score'] < 5)])  # 3-4
        stats['poor_count'] = len(df[df['quality_score'] < 3])  # 0-2

    return stats


def filter_dataframe(
    df: pd.DataFrame,
    min_score: int = 0,
    max_score: int = 8,
    failed_criteria: List[str] = None,
    search_text: str = None
) -> pd.DataFrame:
    """
    Filters the analysis DataFrame based on various criteria.

    Args:
        df: Analysis results DataFrame
        min_score: Minimum quality score
        max_score: Maximum quality score
        failed_criteria: List of criteria that must be failed (False)
        search_text: Text to search in ID, label, or full_text

    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()

    # Filter by score range
    if 'quality_score' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['quality_score'] >= min_score) &
            (filtered_df['quality_score'] <= max_score)
        ]

    # Filter by failed criteria
    if failed_criteria:
        for criterion in failed_criteria:
            if criterion in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[criterion] == False]

    # Filter by search text
    if search_text:
        search_text_lower = search_text.lower()
        mask = (
            filtered_df['id'].str.lower().str.contains(search_text_lower, na=False) |
            filtered_df['label'].str.lower().str.contains(search_text_lower, na=False) |
            filtered_df['full_text'].str.lower().str.contains(search_text_lower, na=False)
        )
        filtered_df = filtered_df[mask]

    return filtered_df


def get_failed_requirements_for_criterion(df: pd.DataFrame, criterion: str) -> pd.DataFrame:
    """
    Gets all requirements that failed a specific criterion.

    Args:
        df: Analysis results DataFrame
        criterion: Name of the criterion (e.g., 'necessary', 'unambiguous')

    Returns:
        DataFrame with only failed requirements for that criterion
    """
    if criterion not in df.columns:
        return pd.DataFrame()

    failed_df = df[df[criterion] == False].copy()

    # Select relevant columns
    cols_to_show = ['id', 'label', 'quality_score', f'{criterion}_justification', 'suggestion', 'full_text']
    cols_to_show = [col for col in cols_to_show if col in failed_df.columns]

    return failed_df[cols_to_show]


def get_top_worst_requirements(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Gets the top N requirements with the lowest quality scores.

    Args:
        df: Analysis results DataFrame
        n: Number of requirements to return

    Returns:
        DataFrame with worst requirements
    """
    if 'quality_score' not in df.columns:
        return pd.DataFrame()

    return df.nsmallest(n, 'quality_score')


def get_top_best_requirements(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Gets the top N requirements with the highest quality scores.

    Args:
        df: Analysis results DataFrame
        n: Number of requirements to return

    Returns:
        DataFrame with best requirements
    """
    if 'quality_score' not in df.columns:
        return pd.DataFrame()

    return df.nlargest(n, 'quality_score')
