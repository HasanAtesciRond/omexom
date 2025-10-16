# Tests Directory

Test files and testing utilities.

## Files

### `test_analyzer.py`
**Analyzer Integration Test**

Tests the complete analysis pipeline:
- RDF/Turtle file parsing
- Azure OpenAI API integration
- ISO 29148 criteria evaluation
- Result validation

**Usage:**
```bash
python tests/test_analyzer.py
```

**What it tests:**
- Environment variable loading (.env)
- RDF parser with real data file
- Analyzer initialization
- Batch processing (2 requirements)
- JSON response parsing
- Quality score calculation
- All 8 ISO 29148 criteria

**Expected Output:**
```
[SUCCESS] Analysis successful! 2 results returned

VS2-BRP-080:
  Quality Score: 7/8
  Necessary: True
  Unambiguous: True
  Complete: True
  Verifiable: True
  Suggestion: [improvement text]
```

## Running Tests

### Quick Test
```bash
cd tests
python test_analyzer.py
```

### Full Integration Test
```bash
# Test with different file sizes
python test_analyzer.py --reqs 10   # 10 requirements
python test_analyzer.py --reqs 50   # 50 requirements
```

## Test Coverage

### ✅ Currently Tested
- RDF parsing functionality
- Azure OpenAI authentication
- Analysis endpoint
- JSON response parsing
- Quality scoring

### ⚠️ Pending Tests
- Streamlit UI components
- Export functionality
- Visualization rendering
- Error handling edge cases
- Large file processing

## Adding New Tests

Create new test files following this pattern:
```python
# test_[component].py
from utils.component import function_to_test

def test_function():
    result = function_to_test(test_data)
    assert result == expected_result
    print("[SUCCESS] Test passed")
```

## Test Data

Test data is located in `../data/input/`:
- Small test file: First 10 requirements
- Medium test file: 50-100 requirements
- Full test file: All 668 requirements

## Continuous Integration

Future: Add CI/CD pipeline with automated testing on commit.
