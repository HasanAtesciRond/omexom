# ISO/IEC/IEEE 29148 Requirements Quality Analyzer - Streamlit App

Een professionele web-applicatie voor het analyseren van requirements kwaliteit volgens de ISO/IEC/IEEE 29148 standaard.

## 🎯 Features

- **Upload & Parsing**: Upload RDF/Turtle bestanden met NEN2660 requirements
- **AI-Powered Analysis**: Azure OpenAI analyseert requirements op 8 ISO 29148 criteria
- **Interactive Dashboard**: Real-time visualisaties met Plotly
- **Detailed Results**: Filterable table met alle requirements en justifications
- **Criteria Deep-Dive**: Per-criterion analyse met donut charts
- **Hierarchy View**: Parent-child relaties visualisatie
- **Multi-Format Export**: Excel, CSV, en JSON downloads

## 📋 ISO 29148 Criteria

De app evalueert requirements op 8 kwaliteitscriteria:

1. ✅ **Necessary** (Noodzakelijk)
2. 🎯 **Unambiguous** (Eenduidig)
3. 📋 **Complete** (Compleet)
4. 1️⃣ **Singular** (Enkelvoudig)
5. 🔧 **Feasible** (Haalbaar)
6. ✔️ **Verifiable** (Verifieerbaar)
7. 🔗 **Traceable** (Traceerbaar)
8. 🎨 **Implementation-free** (Implementatie-onafhankelijk)

## 🚀 Installatie

### Vereisten

- Python 3.10 of hoger
- Azure OpenAI API toegang
- 8GB RAM minimum

### Stap 1: Clone de repository

```bash
cd omexom
```

### Stap 2: Installeer dependencies

```bash
pip install -r streamlit_requirements.txt
```

### Stap 3: Configureer Azure OpenAI

**✅ Optie 1: Gebruik de bestaande .env file (Aanbevolen - Al geconfigureerd!)**

De `.env` file is al aanwezig met de juiste credentials uit het Jupyter notebook. Geen verdere actie nodig!

**Optie 2: Streamlit secrets.toml**

Maak een `.streamlit/secrets.toml` bestand (gebruik het example als template):

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml met je credentials
```

**Optie 3: Configureer via UI**

Start de app en configureer via de sidebar → "🔑 Azure OpenAI Configuratie"

**Prioriteit:** `.env` file → `secrets.toml` → UI configuratie

## ▶️ Start de Applicatie

```bash
streamlit run streamlit_app.py
```

De app opent automatisch in je browser op `http://localhost:8501`

## 📖 Gebruikershandleiding

### 1. Upload Requirements

1. Ga naar de **📤 Upload** pagina
2. Sleep een RDF/Turtle bestand (.txt) in de upload zone
3. Wacht op validatie en parsing
4. Bekijk de preview van je requirements
5. Configureer optioneel een limiet voor testdoeleinden

### 2. Start Analyse

1. Ga naar de **⚙️ Analysis** pagina
2. Controleer de analyse configuratie
3. Klik op **Start ISO 29148 Analyse**
4. Monitor de voortgang via de progress bar
5. Wacht tot de analyse compleet is (~2-3 min per 100 requirements)

### 3. Bekijk Resultaten

**Dashboard (📊):**
- Overzicht met KPI's
- Quality score distributie
- Criteria pass rates
- Parent-child heatmap
- Failure matrix

**Detailed Results (📋):**
- Interactieve tabel met alle requirements
- Filters op score, criteria, tekst
- Expandable requirement cards
- Justifications per criterium
- Improvement suggestions

**Criteria Deep-Dive (🔍):**
- Selecteer een specifiek criterium
- Donut chart met pass/fail ratio
- Lijst van gefaalde requirements
- Gedetailleerde justifications

**Hierarchy View (🌳):**
- Interactive tree diagram
- Parent summary tabel
- Aggregated quality scores per parent
- Best/worst parent rankings

### 4. Exporteer Resultaten

1. Ga naar de **💾 Export** pagina
2. Kies een formaat (Excel, CSV, JSON)
3. Pas optioneel filters toe
4. Download het bestand

## 🏗️ Project Structuur

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
│   ├── rdf_parser.py             # RDF/Turtle parsing
│   ├── analyzer.py               # Azure OpenAI integration
│   ├── visualizations.py         # Plotly charts
│   └── export_utils.py           # Export functions
├── config/
│   ├── settings.py               # App configuration
│   └── criteria_definitions.py   # ISO 29148 definitions
├── streamlit_requirements.txt    # Python dependencies
└── STREAMLIT_README.md           # This file
```

## ⚙️ Configuratie Opties

### Analyse Instellingen

Via de sidebar op de homepage:

- **Batch Size**: Aantal requirements per API call (default: 5)
- **Concurrent Workers**: Aantal parallelle threads (default: 15)
- **Max Completion Tokens**: Maximum tokens per response (default: 10000)

### RDF Parsing

De parser verwacht RDF/Turtle bestanden met de volgende structuur:

```turtle
@prefix nen2660: <https://w3id.org/nen2660/def#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix tennet: <http://data.tennet.eu/def/> .

<requirement/1> a nen2660:Requirement ;
    skos:notation "REQ-001" ;
    skos:prefLabel "System Requirement" ;
    rdf:value "The system shall..." .

<requirement/2> a nen2660:Requirement ;
    skos:notation "REQ-002" ;
    skos:prefLabel "Subsystem Requirement" ;
    rdf:value "The subsystem shall..." .

<requirement/1> tennet:isDerivedIn <requirement/2> .
```

## 🐛 Troubleshooting

### Fout: "Azure OpenAI authentication failed"

**Oplossing:** Controleer je API credentials in de sidebar settings of `.streamlit/secrets.toml`

### Fout: "Invalid TTL/RDF format"

**Oplossing:** Zorg dat je bestand geldig RDF/Turtle formaat heeft en de juiste prefixes bevat

### Fout: "No requirements found"

**Oplossing:** Controleer of je bestand requirements bevat met `a nen2660:Requirement`

### Analyse duurt te lang

**Oplossing:**
- Verlaag het aantal concurrent workers (minder parallel = minder geheugen)
- Gebruik de analysis limit optie om eerst een subset te testen
- Check je Azure OpenAI quota en rate limits

### Out of memory error

**Oplossing:**
- Analyseer requirements in batches (gebruik max_requirements limiet)
- Verlaag concurrent workers naar 5-10
- Sluit andere applicaties

## 📊 Performance

Typische performance metrics:

- **Parsing**: ~100-500 requirements per seconde
- **Analysis**: ~2-3 seconden per requirement (API dependent)
- **Dashboard load**: < 2 seconden
- **Export**: < 5 seconden voor 1000 requirements

## 🔒 Security

- API keys worden NOOIT gelogd of opgeslagen in bestanden
- Session state is per-user en wordt niet gedeeld
- Geen data persistence (alles in memory)
- Uploaded files worden opgeslagen in temp directory en automatisch verwijderd

## 📝 Licentie

Proprietary - Omexom Internal Use Only

## 👥 Contact

Voor vragen of support, neem contact op met het development team.

## 🗺️ Roadmap

**Toekomstige features:**

- PDF export met visualisaties
- Historical comparison tussen analyses
- Custom criteria weights
- User authentication
- Multi-project management
- Scheduled batch analysis
- Integration met Jira/Azure DevOps
- AI-powered automatic requirement improvement

## 📚 Resources

- [ISO/IEC/IEEE 29148:2018 Standard](https://www.iso.org/standard/72146.html)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
