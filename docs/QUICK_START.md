# 🚀 Quick Start Guide - ISO 29148 Requirements Analyzer

Snel aan de slag in 3 stappen!

## ⚡ Super Snelle Start

```bash
# 1. Installeer dependencies
pip install -r streamlit_requirements.txt

# 2. Start de app (credentials zijn al geconfigureerd in .env!)
streamlit run streamlit_app.py

# 3. Open browser: http://localhost:8501
```

**Dat is alles!** De Azure OpenAI credentials zijn al geladen vanuit de `.env` file.

---

## 📋 Volledige Workflow

### Stap 1: Upload Requirements
1. Klik op **📤 Upload** in de sidebar
2. Sleep je `NVD110_VS2_20250709.txt` bestand in de upload zone
3. Klik **🔍 Parseer Requirements**
4. Controleer de preview en statistieken

### Stap 2: Start Analyse
1. Klik op **⚙️ Analysis** in de sidebar
2. (Optioneel) Pas configuratie aan:
   - Zet "Maximum aantal" op 10 voor een snelle test
   - Of laat op 0 voor alle requirements
3. Klik **▶️ Start ISO 29148 Analyse**
4. Wacht op voltooiing (~2-3 min voor 50 reqs)

### Stap 3: Bekijk Resultaten
1. Automatisch naar **📊 Dashboard** na analyse
2. Verken:
   - **📊 Dashboard**: Overzicht en KPI's
   - **📋 Results**: Gedetailleerde tabel met filters
   - **🔍 Criteria**: Deep-dive per ISO criterium
   - **🌳 Hierarchy**: Parent-child relaties
   - **💾 Export**: Download als Excel/CSV/JSON

---

## 🎯 Belangrijke Files

| File | Beschrijving |
|------|--------------|
| `.env` | Azure OpenAI credentials (al geconfigureerd!) |
| `NVD110_VS2_20250709.txt` | Je requirements input file |
| `streamlit_app.py` | Start de app hiermee |
| `streamlit_requirements.txt` | Python dependencies |

---

## ⚙️ Configuratie Check

Als de app start, zie je in de sidebar:
- ✅ Groene vinkje bij "Azure OpenAI Configuratie" = credentials geladen
- ⚠️ Als er een waarschuwing is: check `.env` file

---

## 🐛 Troubleshooting

**App start niet?**
```bash
pip install --upgrade streamlit
pip install -r streamlit_requirements.txt
```

**API errors?**
- Check of `.env` file bestaat
- Controleer credentials in `.env`
- Test via sidebar → "🔑 Azure OpenAI Configuratie"

**Parsing errors?**
- Controleer of TTL file valid is
- Moet `nen2660:Requirement` types bevatten

---

## 💡 Tips

- **Eerste keer?** Test met 10-20 requirements (snel resultaat)
- **Slow analysis?** Verlaag concurrent workers naar 10
- **Out of memory?** Gebruik batch size 5 en max 100 reqs per run
- **Excel export?** Ga naar **💾 Export** pagina na analyse

---

## 📚 Meer Info

Zie [STREAMLIT_README.md](STREAMLIT_README.md) voor:
- Uitgebreide documentatie
- Alle features
- Advanced configuratie
- Troubleshooting details

---

**Veel succes!** 🎉
