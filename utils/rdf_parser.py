"""
RDF/Turtle Parser for Requirements Extraction
Extracts requirements from NEN2660 formatted TTL files with parent-child relationships
"""

import os
import logging
from typing import List, Dict, Optional
from rdflib import Graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def extract_requirements_from_file(file_path: str) -> List[Dict]:
    """
    PHASE 1: THE RDF PARSER (ENHANCED VERSION).
    This function parses the TTL file and identifies parent-child relationships
    between requirements. It enriches each child requirement with the text of its
    parent to provide full context for the LLM analysis.

    Args:
        file_path: The path to the input .txt file (TTL/RDF format).

    Returns:
        A list of dictionaries, where each dictionary represents a requirement
        and includes contextual parent information if available.

    Example return:
        [
            {
                'id': 'REQ-001',
                'label': 'System Requirement',
                'text': 'The system shall...',
                'parent_id': None,
                'parent_text': None
            },
            {
                'id': 'REQ-002',
                'label': 'Subsystem Requirement',
                'text': 'The subsystem shall...',
                'parent_id': 'REQ-001',
                'parent_text': 'The system shall...'
            }
        ]
    """
    if not os.path.exists(file_path):
        logging.error(f"Input file '{file_path}' not found.")
        return []

    logging.info(f"Starting contextual requirement extraction from: {file_path}")

    graph = Graph()
    try:
        graph.parse(file_path, format="turtle")
        logging.info(f"Successfully parsed TTL file with {len(graph)} triples")
    except Exception as e:
        logging.error(f"Failed to parse the Turtle file: {e}")
        return []

    # This SPARQL query finds all requirements and optionally their parent requirements
    query = """
        PREFIX nen2660: <https://w3id.org/nen2660/def#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX tennet: <http://data.tennet.eu/def/>

        SELECT ?req ?notation ?label ?value ?parent_notation ?parent_value
        WHERE {
            ?req a nen2660:Requirement .
            ?req skos:notation ?notation .
            ?req rdf:value ?value .
            OPTIONAL { ?req skos:prefLabel ?label . }

            # Optional: Find a parent that this requirement is derived from
            OPTIONAL {
                ?parent tennet:isDerivedIn ?req .
                ?parent skos:notation ?parent_notation .
                ?parent rdf:value ?parent_value .
            }
        }
    """

    results = graph.query(query)

    requirements_list = []
    for row in results:
        req_text = str(row.value) if row.value else ""
        if req_text.strip():
            requirements_list.append({
                'id': str(row.notation),
                'label': str(row.label) if row.label else "N/A",
                'text': req_text,
                'parent_id': str(row.parent_notation) if row.parent_notation else None,
                'parent_text': str(row.parent_value) if row.parent_value else None,
            })

    logging.info(f"Successfully extracted {len(requirements_list)} requirements with parent context.")
    return requirements_list


def validate_ttl_file(file_path: str) -> tuple[bool, Optional[str]]:
    """
    Validates if a file is a valid Turtle/RDF file.

    Args:
        file_path: Path to the file to validate

    Returns:
        Tuple of (is_valid, error_message)
        If valid: (True, None)
        If invalid: (False, "Error description")
    """
    if not os.path.exists(file_path):
        return False, "File does not exist"

    if not file_path.endswith('.txt'):
        return False, "File must have .txt extension (TTL format)"

    try:
        graph = Graph()
        graph.parse(file_path, format="turtle")

        if len(graph) == 0:
            return False, "File contains no RDF triples"

        return True, None
    except Exception as e:
        return False, f"Invalid TTL/RDF format: {str(e)}"


def get_requirement_statistics(requirements: List[Dict]) -> Dict:
    """
    Calculates statistics about the extracted requirements.

    Args:
        requirements: List of requirement dictionaries

    Returns:
        Dictionary with statistics
    """
    if not requirements:
        return {
            'total_count': 0,
            'with_parent': 0,
            'without_parent': 0,
            'unique_parents': 0,
            'avg_text_length': 0
        }

    with_parent = sum(1 for req in requirements if req.get('parent_id'))
    without_parent = len(requirements) - with_parent
    unique_parents = len(set(req['parent_id'] for req in requirements if req.get('parent_id')))
    avg_length = sum(len(req['text']) for req in requirements) / len(requirements)

    return {
        'total_count': len(requirements),
        'with_parent': with_parent,
        'without_parent': without_parent,
        'unique_parents': unique_parents,
        'avg_text_length': round(avg_length, 1)
    }
