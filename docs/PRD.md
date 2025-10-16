# Product Requirements Document (PRD)
## ISO/IEC/IEEE 29148 Requirements Quality Analyzer - Streamlit Web Application

---

## 1. Executive Summary

**Product Name:** ISO 29148 Requirements Quality Analyzer
**Purpose:** A professional web-based interface for analyzing requirements quality based on ISO/IEC/IEEE 29148 standards
**Target Users:** Systems Engineers, Requirements Engineers, Project Managers, Quality Assurance Teams
**Core Value:** Transform complex RDF/Turtle requirement files into actionable quality insights with interactive visualizations

---

## 2. Current System Analysis

### 2.1 Existing Implementation
- **Backend:** Jupyter Notebook (`SMART_analyzer.ipynb`)
- **Input:** RDF/Turtle (`.txt`) files containing NEN2660 requirements with parent-child relationships
- **Processing:** Azure OpenAI (o3-mini-1 model) for batch analysis
- **Output:** Excel file with two sheets:
  - ISO 29148 Analysis (detailed per-requirement)
  - Parent Summary (aggregated metrics)

### 2.2 Data Flow
```
Input TTL File → RDF Parser → Requirement Extraction →
Batch Processing (Azure OpenAI) → ISO 29148 Analysis →
Excel Output (2 sheets)
```

### 2.3 Key Data Structures

**Input Requirements:**
- ID (notation)
- Label (prefLabel)
- Text content (value)
- Parent ID (isDerivedIn relationship)
- Parent text

**Output Analysis (8 ISO 29148 Criteria):**
1. Necessary (Noodzakelijk)
2. Unambiguous (Eenduidig)
3. Complete (Compleet)
4. Singular (Enkelvoudig)
5. Feasible (Haalbaar)
6. Verifiable (Verifieerbaar)
7. Traceable (Traceerbaar)
8. Implementation-free (Implementatie-onafhankelijk)

Each criterion includes boolean pass/fail + justification + improvement suggestion + quality_score (0-8)

---

## 3. Product Vision

### 3.1 Goals
1. **Accessibility:** Non-technical users can analyze requirements without Jupyter/Python knowledge
2. **Interactivity:** Real-time exploration of analysis results with filtering and drill-down
3. **Actionability:** Clear visualization of issues and improvement opportunities
4. **Professional:** Enterprise-ready UI suitable for client presentations
5. **Efficiency:** Streamlined workflow from upload to insights

### 3.2 Success Metrics
- Upload to first insight: < 30 seconds
- User can identify top 10 problematic requirements: < 2 minutes
- Export customized reports: < 1 minute
- Zero technical support needed for basic operations

---

## 4. Feature Requirements

### 4.1 Core Features (MVP)

#### **F1: File Upload & Validation**
- **Input:** Drag-and-drop or browse for `.txt` (TTL/RDF) files
- **Validation:**
  - File format check (RDF/Turtle parsing)
  - Preview first 5-10 requirements
  - Display total requirement count
- **Configuration:**
  - Analysis limit slider (10-500 requirements, or "All")
  - Batch size setting (default: 5)

#### **F2: Analysis Execution**
- **Process:**
  - Progress bar with batch-level updates
  - Real-time log display (collapsible)
  - Estimated time remaining
  - Cancel/pause option
- **API Configuration:**
  - Azure OpenAI credentials (sidebar, encrypted)
  - Model selection
  - Token limit configuration

#### **F3: Results Dashboard**
- **Overview Metrics (Top KPIs):**
  - Average Quality Score (0-8 gauge)
  - Total Requirements Analyzed
  - Pass Rate per Criterion (8 mini progress bars)
  - Distribution chart (quality score histogram)

#### **F4: Detailed Analysis Table**
- **Interactive Data Table:**
  - All requirements with columns: ID, Label, Quality Score, Parent ID, 8 criteria (✓/✗), Suggestion
  - Sortable by any column
  - Filterable by:
    - Quality score range
    - Failed criteria (multi-select)
    - Text search (ID, label, content)
  - Color coding:
    - Green (7-8), Yellow (5-6), Orange (3-4), Red (0-2)
  - Expandable rows showing full text + justifications

#### **F5: Parent-Child Relationship View**
- **Hierarchical Visualization:**
  - Tree view or Sankey diagram
  - Parent summary table:
    - Parent ID, Text snippet, # Children, Avg Quality Score
  - Click to expand children requirements
  - Highlight problematic branches

#### **F6: Criteria Deep-Dive**
- **Per-Criterion Analysis:**
  - 8 tabs (one per ISO criterion)
  - For each tab:
    - Pass/Fail count
    - List of failed requirements
    - Common failure patterns (word cloud from justifications)
    - Top 5 worst offenders

#### **F7: Export Capabilities**
- **Download Options:**
  - Excel file (original 2-sheet format)
  - CSV (filtered results)
  - PDF report (summary + charts)
  - JSON (raw data for further processing)

### 4.2 Advanced Features (Phase 2)

#### **F8: Historical Comparison**
- Upload multiple analysis files
- Compare quality scores over time
- Regression detection

#### **F9: AI-Powered Suggestions**
- Batch suggestion application
- Suggestion quality voting
- Learn from user edits

#### **F10: Custom Criteria**
- User-defined quality rules
- Weighted scoring
- Industry-specific templates

#### **F11: Collaboration**
- Share analysis via link
- Comments on requirements
- Approval workflow

---

## 5. User Interface Design

### 5.1 Layout Structure

```
┌─────────────────────────────────────────────────────┐
│ HEADER: Logo | Title | Settings ⚙                  │
├──────────┬──────────────────────────────────────────┤
│          │  MAIN CONTENT AREA                       │
│ SIDEBAR  │                                          │
│          │  [Tab 1: Upload & Configure]             │
│ - Upload │  [Tab 2: Analysis Progress]              │
│ - Config │  [Tab 3: Dashboard Overview]             │
│ - Help   │  [Tab 4: Detailed Results]               │
│ - About  │  [Tab 5: Criteria Deep-Dive]             │
│          │  [Tab 6: Parent-Child View]              │
│          │  [Tab 7: Export]                         │
└──────────┴──────────────────────────────────────────┘
```

### 5.2 Color Palette (Professional)
- **Primary:** Deep Blue (#1E3A8A) - Headers, key actions
- **Secondary:** Teal (#0D9488) - Highlights, success states
- **Accent:** Amber (#F59E0B) - Warnings, attention items
- **Danger:** Red (#DC2626) - Errors, critical issues
- **Success:** Green (#10B981) - Passed criteria
- **Neutral:** Gray (#6B7280) - Text, borders

### 5.3 Key Components

#### Dashboard Cards
```
┌─────────────────────────┐
│  📊 Avg Quality Score   │
│      6.2 / 8.0          │
│  ████████░░ 78%         │
└─────────────────────────┘
```

#### Requirement Card
```
┌────────────────────────────────────────────┐
│ REQ-001 | Quality: 5/8 ⚠                   │
│ Label: "System shall provide..."           │
│ ✓ Necessary  ✓ Unambiguous  ✗ Complete    │
│ ✗ Singular   ✓ Feasible     ✓ Verifiable  │
│ ✓ Traceable  ✗ Impl-Free                  │
│ 💡 Suggestion: Split into 2 requirements   │
└────────────────────────────────────────────┘
```

---

## 6. Technical Architecture

### 6.1 Technology Stack
- **Frontend Framework:** Streamlit (Python)
- **Data Processing:** pandas, rdflib
- **Visualization:** plotly, altair, streamlit-echarts
- **AI Integration:** openai (Azure OpenAI SDK)
- **Export:** openpyxl, reportlab (PDF), streamlit-aggrid

### 6.2 Architecture Diagram
```
┌─────────────────────────────────────────┐
│         Streamlit UI Layer              │
│  (File Upload, Visualization, Export)   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│      Business Logic Layer               │
│  - RDF Parser (extract_requirements)    │
│  - Batch Manager (process_batches)      │
│  - Results Aggregator                   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│      External Services                  │
│  - Azure OpenAI API                     │
│  - File System (temp storage)           │
└─────────────────────────────────────────┘
```

### 6.3 State Management
- **Session State:**
  - Uploaded file path
  - Parsed requirements
  - Analysis results (DataFrame)
  - User filters/selections
  - API configuration
- **Caching:**
  - RDF parsing (@st.cache_data)
  - Analysis results (@st.cache_data)
  - Visualization generation (@st.cache_resource)

---

## 7. File Structure

```
omexom/
├── streamlit_app.py              # Main entry point
├── pages/
│   ├── 1_📤_Upload.py            # Upload & configure
│   ├── 2_⚙️_Analysis.py          # Run analysis
│   ├── 3_📊_Dashboard.py         # Overview metrics
│   ├── 4_📋_Results.py           # Detailed table
│   ├── 5_🔍_Criteria.py          # Per-criterion view
│   ├── 6_🌳_Hierarchy.py         # Parent-child view
│   └── 7_💾_Export.py            # Download options
├── utils/
│   ├── rdf_parser.py             # extract_requirements_from_file
│   ├── analyzer.py               # analyze_batch_with_llm
│   ├── visualizations.py         # Chart generators
│   └── export_utils.py           # Excel/PDF/CSV export
├── config/
│   ├── settings.py               # Constants, API config
│   └── criteria_definitions.py   # ISO 29148 criteria text
├── assets/
│   ├── logo.png
│   └── styles.css
├── requirements.txt
└── README.md
```

---

## 8. Data Flow Specifications

### 8.1 Upload Phase
```python
Input: TTL file
↓
Validate format (rdflib parse)
↓
Extract requirements → List[Dict]
  {id, label, text, parent_id, parent_text}
↓
Store in st.session_state['requirements']
↓
Display preview table
```

### 8.2 Analysis Phase
```python
User clicks "Analyze"
↓
Create batches (size=5)
↓
For each batch (parallel):
  - Send to Azure OpenAI
  - Parse JSON response
  - Update progress bar
↓
Aggregate results → DataFrame
↓
Store in st.session_state['analysis_df']
↓
Navigate to Dashboard
```

### 8.3 Visualization Phase
```python
Load analysis_df
↓
Apply user filters
↓
Generate visualizations:
  - Quality score distribution (histogram)
  - Criteria pass rates (bar chart)
  - Parent summary (treemap)
  - Failure heatmap (8 criteria × requirements)
↓
Display interactive charts
```

---

## 9. Key Visualizations

### 9.1 Dashboard Charts

**Chart 1: Quality Score Distribution**
- Type: Histogram
- X-axis: Quality Score (0-8)
- Y-axis: Count of Requirements
- Color: Green→Yellow→Red gradient

**Chart 2: Criteria Pass Rate**
- Type: Horizontal Bar Chart
- Bars: 8 ISO criteria
- Values: % passed
- Threshold line at 80%

**Chart 3: Parent-Child Quality Heatmap**
- Type: Treemap
- Size: Number of children
- Color: Average quality score
- Hover: Parent ID + Avg score

**Chart 4: Failure Matrix**
- Type: Heatmap
- Rows: Requirements (top 50 worst)
- Columns: 8 Criteria
- Cell color: Red (fail), Green (pass)

### 9.2 Detail Views

**Criteria Tabs:**
- Donut chart: Pass/Fail ratio
- Table: Failed requirements with justifications
- Word cloud: Common issues from justifications

**Hierarchy View:**
- Interactive tree diagram (using plotly)
- Node size: Number of children
- Node color: Quality score
- Click to expand/collapse branches

---

## 10. User Workflows

### 10.1 Primary Workflow (Happy Path)
1. User opens app → Lands on Upload page
2. Drags TTL file into dropzone
3. Preview shows 10 sample requirements
4. Adjusts settings (limit to 100 reqs, batch=5)
5. Clicks "Start Analysis"
6. Progress bar updates (batch 1/20... 2/20...)
7. Analysis completes → Auto-navigate to Dashboard
8. Views overview: Avg score 6.5/8, 85% Verifiable pass rate
9. Switches to Results tab
10. Filters for quality_score < 5
11. Sees 15 requirements
12. Clicks expand on REQ-042
13. Reads justifications, copies suggestion
14. Exports filtered results as CSV
15. Downloads report

### 10.2 Error Handling Workflow
1. User uploads invalid file (not TTL)
2. Error message: "File format not recognized. Please upload RDF/Turtle (.txt) file"
3. User uploads correct file with 0 requirements
4. Warning: "No requirements found in file. Check file content."
5. User uploads valid file
6. Analysis starts but API key invalid
7. Error: "Azure OpenAI authentication failed. Check API key in Settings."
8. User updates API key in sidebar
9. Retries analysis → Success

---

## 11. Non-Functional Requirements

### 11.1 Performance
- Upload file < 50MB: Parse in < 5s
- Analyze 100 requirements: < 3 minutes (API dependent)
- Dashboard load time: < 2s
- Filter/sort operations: < 500ms

### 11.2 Usability
- Zero-training for basic operations
- Tooltips on all criteria explaining ISO 29148 definitions
- Responsive design (desktop-first, 1920×1080 optimized)
- Multi-language support (Dutch/English toggle)

### 11.3 Security
- API keys stored in st.secrets or environment variables
- No data persistence by default (session-only)
- Option to clear all data on logout
- No requirement text logged to external services

### 11.4 Scalability
- Handle up to 10,000 requirements (paginated views)
- Concurrent API calls (15 workers) via ThreadPoolExecutor
- Chunked Excel export for large datasets

---

## 12. Future Enhancements (Roadmap)

### Phase 1 (MVP) - Weeks 1-4
- F1-F7 implementation
- Core visualizations
- Basic export

### Phase 2 (Enhanced) - Weeks 5-8
- Advanced filters
- Comparative analysis
- PDF reports with branding

### Phase 3 (Enterprise) - Weeks 9-12
- User authentication
- Multi-project management
- API rate limit handling
- Scheduled batch jobs

### Phase 4 (AI-Powered) - Future
- Automatic requirement improvement (GPT-4)
- Predictive quality scoring
- Industry benchmarking
- Integration with Jira/Azure DevOps

---

## 13. Dependencies & Prerequisites

### Required Libraries
```
streamlit>=1.30.0
pandas>=2.0.0
rdflib>=7.0.0
openai>=1.0.0
plotly>=5.18.0
openpyxl>=3.1.0
streamlit-aggrid>=0.3.4
tqdm>=4.66.0
```

### External Services
- Azure OpenAI API (o3-mini-1 model access)
- Minimum 15 RPM (requests per minute) quota

### Environment
- Python 3.10+
- 8GB RAM minimum
- Modern browser (Chrome, Firefox, Edge)

---

## 14. Success Criteria

**MVP Launch Ready When:**
- [ ] User can upload TTL file and see preview
- [ ] Analysis completes without errors for 100-req file
- [ ] Dashboard shows 4 key charts
- [ ] Results table is filterable and sortable
- [ ] Excel export matches original format
- [ ] Zero crashes in 10 consecutive runs
- [ ] UI passes accessibility check (WCAG 2.1 Level A)

**Product-Market Fit When:**
- [ ] 5 stakeholders can complete workflow independently
- [ ] Analysis time < 50% of manual review time
- [ ] 80% of identified issues match expert review
- [ ] Positive feedback from 4/5 beta users

---

## 15. Open Questions & Decisions Needed

1. **Authentication:** Do we need user login, or single-instance deployment?
2. **Data Persistence:** Should analysis history be saved to database?
3. **Branding:** Custom logo/colors per client deployment?
4. **Pricing Model:** SaaS vs. on-premise license?
5. **Language:** Dutch-first or bilingual UI?

---

**Document Version:** 1.0
**Created:** 2025-10-16
**Author:** Requirements Analysis Team
**Status:** Draft for Review
