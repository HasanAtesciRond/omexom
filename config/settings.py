"""
Configuration settings for ISO 29148 Requirements Analyzer
"""

# Azure OpenAI Configuration
DEFAULT_AZURE_ENDPOINT = "https://salesassistantllm.openai.azure.com/"
DEFAULT_API_VERSION = "2024-12-01-preview"
DEFAULT_MODEL_NAME = "o3-mini-1"

# Analysis Configuration
DEFAULT_BATCH_SIZE = 5
DEFAULT_MAX_COMPLETION_TOKENS = 10000
DEFAULT_CONCURRENT_WORKERS = 15
DEFAULT_MAX_REQUIREMENTS = None  # None means analyze all

# File Upload Configuration
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = ['.txt']
PREVIEW_ROWS = 10

# UI Configuration
PAGE_TITLE = "ISO 29148 Requirements Quality Analyzer"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Color Palette
COLORS = {
    'primary': '#1E3A8A',      # Deep Blue
    'secondary': '#0D9488',    # Teal
    'accent': '#F59E0B',       # Amber
    'danger': '#DC2626',       # Red
    'success': '#10B981',      # Green
    'warning': '#FCD34D',      # Yellow
    'neutral': '#6B7280',      # Gray
}

# Quality Score Thresholds
QUALITY_THRESHOLDS = {
    'excellent': (7, 8),   # Green
    'good': (5, 6),        # Yellow
    'fair': (3, 4),        # Orange
    'poor': (0, 2),        # Red
}

# Session State Keys
SESSION_KEYS = {
    'uploaded_file': 'uploaded_file_path',
    'requirements': 'parsed_requirements',
    'analysis_results': 'analysis_df',
    'analyzer_config': 'analyzer_config',
    'analysis_in_progress': 'analysis_running',
}

# Export Configuration
EXPORT_FORMATS = ['Excel (.xlsx)', 'CSV', 'JSON']
EXCEL_FILENAME = 'ISO29148_Analysis_Results.xlsx'
CSV_FILENAME = 'ISO29148_Analysis_Results.csv'
JSON_FILENAME = 'ISO29148_Analysis_Results.json'
