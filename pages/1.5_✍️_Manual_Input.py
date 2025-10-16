"""
Manual Requirement Input Page
Allows users to manually enter custom requirements or bulk import from CSV/Excel
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from config.settings import SESSION_KEYS

st.set_page_config(page_title="Manual Input", page_icon="✍️", layout="wide")

st.title("✍️ Handmatige Requirement Invoer")
st.markdown("Voer zelf requirements in of upload ze via CSV/Excel")

# Initialize custom requirements in session state
if 'custom_requirements' not in st.session_state:
    st.session_state['custom_requirements'] = []

# Initialize counter for auto-generated IDs
if 'custom_req_counter' not in st.session_state:
    st.session_state['custom_req_counter'] = 1

# Tabs for different input methods
tab1, tab2, tab3 = st.tabs(["📝 Enkele Requirement", "📊 Bulk Import (CSV/Excel)", "👀 Preview & Beheer"])

# Tab 1: Single requirement input
with tab1:
    st.markdown("### Voeg een nieuwe requirement toe")

    with st.form("single_requirement_form"):
        col1, col2 = st.columns([2, 1])

        with col1:
            req_id = st.text_input(
                "Requirement ID*",
                value=f"CUSTOM-{st.session_state['custom_req_counter']:03d}",
                help="Unieke identifier voor deze requirement"
            )

            req_text = st.text_area(
                "Requirement Tekst*",
                height=150,
                help="De volledige tekst van de requirement",
                placeholder="Bijvoorbeeld: Het systeem moet binnen 2 seconden reageren op gebruikersinvoer..."
            )

        with col2:
            req_label = st.text_input(
                "Label/Titel",
                help="Korte beschrijving of titel (optioneel)",
                placeholder="Response Time Requirement"
            )

            parent_id = st.text_input(
                "Parent Requirement ID",
                help="ID van parent requirement (optioneel, voor hiërarchie)",
                placeholder="Bijvoorbeeld: CUSTOM-001"
            )

            parent_text = st.text_area(
                "Parent Tekst",
                height=80,
                help="Tekst van parent requirement (optioneel)",
                placeholder="Als deze requirement een child is..."
            )

        submitted = st.form_submit_button("➕ Voeg Toe", type="primary", use_container_width=True)

        if submitted:
            if not req_id or not req_text:
                st.error("❌ Requirement ID en Tekst zijn verplicht!")
            else:
                # Check for duplicate ID
                existing_ids = [r['id'] for r in st.session_state['custom_requirements']]
                if req_id in existing_ids:
                    st.error(f"❌ Requirement ID '{req_id}' bestaat al! Kies een unieke ID.")
                else:
                    # Create new requirement
                    new_req = {
                        'id': req_id,
                        'label': req_label if req_label else "Custom Requirement",
                        'text': req_text,
                        'parent_id': parent_id if parent_id else None,
                        'parent_text': parent_text if parent_text else None,
                        'source': 'manual',
                        'created_at': datetime.now().isoformat()
                    }

                    st.session_state['custom_requirements'].append(new_req)
                    st.session_state['custom_req_counter'] += 1

                    st.success(f"✅ Requirement '{req_id}' toegevoegd!")
                    st.rerun()

# Tab 2: Bulk import
with tab2:
    st.markdown("### 📊 Bulk Import via CSV/Excel")

    # Download template
    st.markdown("#### 1. Download Template")

    col1, col2 = st.columns(2)

    with col1:
        # Create CSV template
        template_df = pd.DataFrame({
            'id': ['CUSTOM-001', 'CUSTOM-002', 'CUSTOM-003'],
            'label': ['Example Requirement 1', 'Example Requirement 2', 'Example Requirement 3'],
            'text': [
                'Het systeem moet binnen 2 seconden reageren...',
                'De applicatie moet voldoen aan GDPR wetgeving...',
                'Alle gebruikersdata moet encrypted worden opgeslagen...'
            ],
            'parent_id': ['', 'CUSTOM-001', 'CUSTOM-001'],
            'parent_text': ['', 'Parent tekst hier...', 'Parent tekst hier...']
        })

        csv_buffer = io.StringIO()
        template_df.to_csv(csv_buffer, index=False)

        st.download_button(
            label="📥 Download CSV Template",
            data=csv_buffer.getvalue(),
            file_name="requirements_template.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # Create Excel template
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            template_df.to_excel(writer, index=False, sheet_name='Requirements')

        st.download_button(
            label="📥 Download Excel Template",
            data=excel_buffer.getvalue(),
            file_name="requirements_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("---")

    # Upload file
    st.markdown("#### 2. Upload Ingevuld Bestand")

    uploaded_file = st.file_uploader(
        "Kies een CSV of Excel bestand",
        type=['csv', 'xlsx'],
        help="Upload een bestand met requirements volgens het template formaat"
    )

    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Validate columns
            required_cols = ['id', 'text']
            if not all(col in df.columns for col in required_cols):
                st.error(f"❌ Bestand moet tenminste deze kolommen bevatten: {', '.join(required_cols)}")
            else:
                st.success(f"✅ Bestand geladen: {len(df)} requirements gevonden")

                # Preview
                st.markdown("#### 3. Preview")
                st.dataframe(df.head(10), use_container_width=True)

                # Import button
                if st.button("📥 Importeer Requirements", type="primary"):
                    imported_count = 0
                    duplicate_count = 0
                    error_count = 0

                    existing_ids = [r['id'] for r in st.session_state['custom_requirements']]

                    for idx, row in df.iterrows():
                        req_id = str(row['id']).strip()
                        req_text = str(row['text']).strip()

                        if not req_id or not req_text or req_text == 'nan':
                            error_count += 1
                            continue

                        if req_id in existing_ids:
                            duplicate_count += 1
                            continue

                        new_req = {
                            'id': req_id,
                            'label': str(row.get('label', 'Imported Requirement')),
                            'text': req_text,
                            'parent_id': str(row.get('parent_id', '')) if pd.notna(row.get('parent_id')) else None,
                            'parent_text': str(row.get('parent_text', '')) if pd.notna(row.get('parent_text')) else None,
                            'source': 'bulk_import',
                            'created_at': datetime.now().isoformat()
                        }

                        st.session_state['custom_requirements'].append(new_req)
                        existing_ids.append(req_id)
                        imported_count += 1

                    # Show results
                    st.success(f"✅ {imported_count} requirements geïmporteerd")
                    if duplicate_count > 0:
                        st.warning(f"⚠️ {duplicate_count} duplicaten overgeslagen")
                    if error_count > 0:
                        st.error(f"❌ {error_count} requirements met fouten overgeslagen")

                    st.rerun()

        except Exception as e:
            st.error(f"❌ Fout bij lezen bestand: {str(e)}")

# Tab 3: Preview and management
with tab3:
    st.markdown("### 👀 Huidige Custom Requirements")

    if not st.session_state['custom_requirements']:
        st.info("📭 Nog geen custom requirements toegevoegd. Gebruik de andere tabs om requirements toe te voegen.")
    else:
        # Statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Totaal Custom Requirements", len(st.session_state['custom_requirements']))

        with col2:
            with_parent = sum(1 for r in st.session_state['custom_requirements'] if r['parent_id'])
            st.metric("Met Parent", with_parent)

        with col3:
            manual_count = sum(1 for r in st.session_state['custom_requirements'] if r.get('source') == 'manual')
            st.metric("Handmatig Toegevoegd", manual_count)

        st.markdown("---")

        # Display requirements
        st.markdown("#### Requirements Lijst")

        for idx, req in enumerate(st.session_state['custom_requirements']):
            with st.expander(f"{req['id']} - {req['label'][:50]}..."):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**ID:** {req['id']}")
                    st.markdown(f"**Label:** {req['label']}")
                    st.markdown(f"**Text:** {req['text']}")
                    if req['parent_id']:
                        st.markdown(f"**Parent ID:** {req['parent_id']}")
                        if req['parent_text']:
                            st.markdown(f"**Parent Text:** {req['parent_text'][:100]}...")
                    st.markdown(f"**Bron:** {req.get('source', 'unknown')}")
                    st.markdown(f"**Toegevoegd op:** {req.get('created_at', 'Unknown')[:19]}")

                with col2:
                    if st.button("🗑️ Verwijder", key=f"delete_{idx}"):
                        st.session_state['custom_requirements'].pop(idx)
                        st.rerun()

        st.markdown("---")

        # Export custom requirements
        st.markdown("#### 📥 Exporteer Custom Requirements")

        col1, col2, col3 = st.columns(3)

        with col1:
            # CSV export
            df_export = pd.DataFrame(st.session_state['custom_requirements'])
            csv_export = df_export.to_csv(index=False)

            st.download_button(
                "📥 Download als CSV",
                data=csv_export,
                file_name=f"custom_requirements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            # Excel export
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df_export.to_excel(writer, index=False, sheet_name='Custom Requirements')

            st.download_button(
                "📥 Download als Excel",
                data=excel_buffer.getvalue(),
                file_name=f"custom_requirements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with col3:
            # Clear all
            if st.button("🗑️ Verwijder Alles", type="secondary", use_container_width=True):
                st.session_state['custom_requirements'] = []
                st.rerun()

# Merge section
st.markdown("---")
st.markdown("### 🔗 Integratie met RDF Requirements")

merge_option = st.radio(
    "Hoe wil je custom requirements gebruiken?",
    options=[
        "merge_with_rdf",
        "custom_only",
        "rdf_only"
    ],
    format_func=lambda x: {
        "merge_with_rdf": "📎 Samenvoegen - Combineer custom requirements met RDF requirements",
        "custom_only": "✍️ Alleen Custom - Gebruik alleen handmatig ingevoerde requirements",
        "rdf_only": "📤 Alleen RDF - Gebruik alleen uploaded RDF requirements"
    }[x],
    help="Bepaal welke requirements gebruikt worden voor analyse"
)

st.session_state['requirement_merge_mode'] = merge_option

# Show combined statistics
if merge_option == "merge_with_rdf":
    rdf_count = len(st.session_state.get(SESSION_KEYS['requirements'], []) or [])
    custom_count = len(st.session_state['custom_requirements'])
    total = rdf_count + custom_count

    st.info(f"""
    📊 **Gecombineerde Requirements:**
    - RDF Requirements: {rdf_count}
    - Custom Requirements: {custom_count}
    - **Totaal voor analyse: {total}**
    """)

# Navigation
st.markdown("---")
st.markdown("### ✅ Volgende Stap")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    total_reqs = 0

    if merge_option == "merge_with_rdf":
        rdf_count = len(st.session_state.get(SESSION_KEYS['requirements'], []) or [])
        custom_count = len(st.session_state['custom_requirements'])
        total_reqs = rdf_count + custom_count
    elif merge_option == "custom_only":
        total_reqs = len(st.session_state['custom_requirements'])
    elif merge_option == "rdf_only":
        total_reqs = len(st.session_state.get(SESSION_KEYS['requirements'], []) or [])

    if total_reqs > 0:
        st.success(f"""
        ✅ {total_reqs} requirement(s) klaar voor analyse!

        Ga naar de **⚙️ Analysis** pagina om de analyse te starten.
        """)

        if st.button("➡️ Naar Analyse Pagina", type="primary", use_container_width=True):
            st.switch_page("pages/2_⚙️_Analysis.py")
    else:
        st.warning("""
        ⚠️ Geen requirements geselecteerd voor analyse.

        Voeg custom requirements toe of upload een RDF bestand.
        """)

# Sidebar info
with st.sidebar:
    st.markdown("### ✍️ Manual Input Status")

    custom_count = len(st.session_state['custom_requirements'])
    if custom_count > 0:
        st.success(f"✅ {custom_count} custom requirement(s)")
    else:
        st.warning("⏳ Geen custom requirements")

    st.markdown("---")

    merge_mode = st.session_state.get('requirement_merge_mode', 'merge_with_rdf')
    mode_display = {
        "merge_with_rdf": "📎 Merge Mode",
        "custom_only": "✍️ Custom Only",
        "rdf_only": "📤 RDF Only"
    }
    st.info(f"**Mode:** {mode_display[merge_mode]}")
