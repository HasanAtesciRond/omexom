"""Quick test of the analyzer with 2 requirements"""
import os
from dotenv import load_dotenv
from utils.rdf_parser import extract_requirements_from_file
from utils.analyzer import RequirementsAnalyzer

# Load environment variables
load_dotenv()

print("Loading requirements...")
requirements = extract_requirements_from_file('NVD110_VS2_20250709.txt')
print(f"Loaded {len(requirements)} requirements")

# Test with just 2 requirements
test_reqs = requirements[:2]
print(f"\nTesting with {len(test_reqs)} requirements:")
for req in test_reqs:
    print(f"  - {req['id']}: {req['text'][:50]}...")

# Create analyzer
print("\nInitializing analyzer...")
analyzer = RequirementsAnalyzer(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    model_name=os.getenv('AZURE_OPENAI_MODEL_NAME'),
    batch_size=5,
    max_completion_tokens=10000,
    concurrent_workers=1  # Just 1 for testing
)

print("\nStarting analysis...")
results = analyzer.analyze_requirements(test_reqs, max_requirements=2)

if results:
    print(f"\n[SUCCESS] Analysis successful! {len(results)} results returned")
    for result in results:
        print(f"\n{result['id']}:")
        print(f"  Quality Score: {result.get('quality_score', 'N/A')}/8")
        print(f"  Necessary: {result.get('necessary', 'N/A')}")
        print(f"  Unambiguous: {result.get('unambiguous', 'N/A')}")
        print(f"  Complete: {result.get('complete', 'N/A')}")
        print(f"  Verifiable: {result.get('verifiable', 'N/A')}")
        suggestion = result.get('suggestion', 'N/A')
        if len(suggestion) > 100:
            suggestion = suggestion[:100] + "..."
        print(f"  Suggestion: {suggestion}")
else:
    print("\n[FAILED] Analysis failed - no results")
