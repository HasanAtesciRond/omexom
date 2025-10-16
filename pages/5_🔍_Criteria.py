"""
Criteria Deep-Dive Page with Custom Requirement Input
Per-criterion analysis, ISO 29148 criteria reference, and manual requirement entry
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils.visualizations import create_donut_chart
from utils.export_utils import get_failed_requirements_for_criterion
from config.settings import SESSION_KEYS
from config.criteria_definitions import CRITERIA, CRITERIA_ORDER, get_criterion_info

st.set_page_config(page_title="Criteria & Input", page_icon="🔍", layout="wide")

st.title("🔍 ISO 29148 Criteria & Custom Requirements")
st.markdown("Criteria analyse, referentie informatie en handmatige requirement invoer")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["📖 Criteria Referentie", "📊 Criteria Analyse", "✍️ Custom Requirements"])

# Tab 1: Criteria Reference (Always visible)
with tab1:
    st.markdown("### 📚 ISO/IEC/IEEE 29148 Kwaliteitscriteria")

    st.info("""
    Deze 8 criteria worden gebruikt door de LLM om elke requirement te analyseren.
    Alle criteria moeten 'true' zijn voor een perfecte score van 8/8.
    """)

    for idx, criterion in enumerate(CRITERIA_ORDER, 1):
        info = CRITERIA[criterion]

        with st.expander(f"{idx}. {info['icon']} {info['name_nl'].upper()} - {info['name_en']}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Nederlandse naam:** {info['name_nl']}")
                st.markdown(f"**Engelse naam:** {info['name_en']}")
                st.markdown(f"**Vraag:** {info['question_nl']}")
                st.markdown(f"**Beschrijving:** {info['description_nl']}")
                st.markdown(f"**Richtlijn:** {info['guidance_nl']}")

            with col2:
                st.markdown("**Voorbeelden:**")

                # Good example
                if 'example_good' in info:
                    st.success(f"✅ **Goed:**\n\n{info['example_good']}")

                # Bad example
                if 'example_bad' in info:
                    st.error(f"❌ **Fout:**\n\n{info['example_bad']}")

    st.markdown("---")
    st.markdown("""
    ### 💡 LLM Prompt

    Deze criteria worden letterlijk in de LLM system prompt gebruikt:

    ```
    Evalueer elke eis op de volgende ISO/IEC/IEEE 29148 kwaliteitscriteria:

    1. NECESSARY (Noodzakelijk): Is de eis noodzakelijk en voegt deze waarde toe aan het systeem?
    2. UNAMBIGUOUS (Eenduidig): Is de eis duidelijk geformuleerd zonder ruimte voor meerdere interpretaties?
    3. COMPLETE (Compleet): Bevat de eis alle noodzakelijke informatie zonder TBD's of open punten?
    4. SINGULAR (Enkelvoudig): Beschrijft de eis slechts één specifieke eis (geen 'en/of' constructies)?
    5. FEASIBLE (Haalbaar): Is de eis technisch en economisch realiseerbaar binnen de context?
    6. VERIFIABLE (Verifieerbaar): Kan de eis objectief getest of geverifieerd worden?
    7. TRACEABLE (Traceerbaar): Is de eis identificeerbaar en traceerbaar?
    8. IMPLEMENTATION_FREE (Implementatie-onafhankelijk): Beschrijft de eis WAT er nodig is, niet HOE het moet worden geïmplementeerd?
    ```

    De LLM geeft voor elk criterium een boolean (true/false) en een justification in het Nederlands.
    """)

    st.markdown("---")
    st.markdown("### 🎨 Custom Criteria (Experimental)")

    st.info("""
    **Nieuw!** Je kunt nu je eigen kwaliteitscriteria definiëren.
    Een LLM zal automatisch de analysis prompt aanpassen op basis van jouw custom criteria.
    """)

    # Initialize custom criteria in session state
    if 'custom_criteria' not in st.session_state:
        st.session_state['custom_criteria'] = []

    if 'use_custom_criteria' not in st.session_state:
        st.session_state['use_custom_criteria'] = False

    # Toggle for using custom criteria
    use_custom = st.checkbox(
        "🔄 Gebruik Custom Criteria voor Analyse",
        value=st.session_state['use_custom_criteria'],
        help="Wanneer aangevinkt, worden jouw custom criteria gebruikt i.p.v. ISO 29148"
    )
    st.session_state['use_custom_criteria'] = use_custom

    if not use_custom:
        st.warning("⚠️ Custom criteria zijn UITGESCHAKELD. De standaard ISO 29148 criteria worden gebruikt.")
    else:
        st.success("✅ Custom criteria zijn INGESCHAKELD. Jouw criteria worden gebruikt voor analyse.")

    # Show current custom criteria
    custom_crit_col1, custom_crit_col2 = st.columns([2, 1])

    with custom_crit_col1:
        st.markdown("#### 📝 Huidige Custom Criteria")

        if not st.session_state['custom_criteria']:
            st.info("Nog geen custom criteria gedefinieerd.")
        else:
            for idx, criterion in enumerate(st.session_state['custom_criteria']):
                with st.expander(f"{idx+1}. {criterion['name']}"):
                    st.markdown(f"**Naam:** {criterion['name']}")
                    st.markdown(f"**Beschrijving:** {criterion['description']}")
                    if criterion.get('guidance'):
                        st.markdown(f"**Guidance:** {criterion['guidance']}")

                    if st.button("🗑️ Verwijder", key=f"del_crit_{idx}"):
                        st.session_state['custom_criteria'].pop(idx)
                        st.rerun()

    with custom_crit_col2:
        st.markdown("#### ➕ Nieuw Criterium")

        with st.form("add_custom_criterion"):
            crit_name = st.text_input(
                "Criterium Naam*",
                placeholder="Bijvoorbeeld: Security",
                help="Naam van het kwaliteitscriterium"
            )

            crit_desc = st.text_area(
                "Beschrijving*",
                height=100,
                placeholder="Bijvoorbeeld: De requirement moet voldoen aan security best practices...",
                help="Wat evalueert dit criterium?"
            )

            crit_guidance = st.text_area(
                "Guidance (optioneel)",
                height=80,
                placeholder="Bijvoorbeeld: Check op gebruik van encryption, authentication, authorization...",
                help="Hoe moet dit criterium geëvalueerd worden?"
            )

            add_criterion_btn = st.form_submit_button("➕ Voeg Criterium Toe", use_container_width=True)

            if add_criterion_btn:
                if not crit_name or not crit_desc:
                    st.error("❌ Naam en Beschrijving zijn verplicht!")
                else:
                    new_criterion = {
                        'name': crit_name.strip(),
                        'description': crit_desc.strip(),
                        'guidance': crit_guidance.strip() if crit_guidance else None,
                        'created_at': datetime.now().isoformat()
                    }

                    st.session_state['custom_criteria'].append(new_criterion)
                    st.success(f"✅ Criterium '{crit_name}' toegevoegd!")
                    st.rerun()

    # Generate/Preview prompt button
    if st.session_state['custom_criteria'] and use_custom:
        st.markdown("---")
        st.markdown("#### 🤖 LLM-Generated Prompt Preview")

        if st.button("🔄 Genereer Preview van Aangepaste Prompt", type="primary"):
            from utils.prompt_generator import PromptGenerator
            from config.settings import SESSION_KEYS

            config = st.session_state.get(SESSION_KEYS['analyzer_config'])

            if not config or not config['azure_endpoint'] or not config['api_key']:
                st.error("❌ Azure OpenAI niet geconfigureerd. Ga naar de homepage om credentials in te stellen.")
            else:
                with st.spinner("🤖 LLM genereert aangepaste prompt..."):
                    try:
                        generator = PromptGenerator(
                            azure_endpoint=config['azure_endpoint'],
                            api_key=config['api_key'],
                            api_version=config['api_version'],
                            model_name=config['model_name']
                        )

                        generated_prompt = generator.generate_custom_prompt(st.session_state['custom_criteria'])

                        st.success("✅ Prompt gegenereerd!")

                        # Store in session state for use in analysis
                        st.session_state['generated_custom_prompt'] = generated_prompt

                        # Display the generated prompt
                        with st.expander("👁️ Bekijk Gegenereerde Prompt", expanded=True):
                            st.code(generated_prompt, language="text")

                        st.info("💾 Deze prompt wordt automatisch gebruikt wanneer je de analyse start met 'Gebruik Custom Criteria' aangevinkt.")

                    except Exception as e:
                        st.error(f"❌ Fout bij genereren prompt: {str(e)}")

    elif st.session_state['custom_criteria'] and not use_custom:
        st.warning("⚠️ Je hebt custom criteria gedefinieerd, maar ze zijn niet actief. Vink 'Gebruik Custom Criteria' aan om ze te gebruiken.")

# Tab 2: Criteria Analysis (Only if results exist)
with tab2:
    # Check if analysis results exist
    if st.session_state.get(SESSION_KEYS['analysis_results']) is None:
        st.warning("⚠️ Geen analyse resultaten gevonden. Voer eerst een analyse uit.")
        if st.button("➡️ Naar Analyse Pagina"):
            st.switch_page("pages/2_⚙️_Analysis.py")
    else:
        df = st.session_state[SESSION_KEYS['analysis_results']]

        st.markdown("### 📊 Gedetailleerde Analyse per Criterium")

        # Criterion selection
        selected_criterion = st.selectbox(
            "Selecteer een criterium",
            options=CRITERIA_ORDER,
            format_func=lambda x: f"{CRITERIA[x]['icon']} {CRITERIA[x]['name_nl']}"
        )

        # Get criterion info
        criterion_info = get_criterion_info(selected_criterion, language='nl')

        # Display criterion information
        st.markdown(f"## {criterion_info['icon']} {criterion_info['name']}")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**Beschrijving:** {criterion_info['description']}")
            st.markdown(f"**Richtlijn:** {criterion_info['guidance']}")

        with col2:
            # Donut chart
            pass_count = df[selected_criterion].sum()
            fail_count = len(df) - pass_count

            fig = create_donut_chart(pass_count, fail_count, criterion_info['name'])
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Statistics
        st.markdown("### 📊 Statistieken")

        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

        with stat_col1:
            st.metric("Totaal Requirements", len(df))

        with stat_col2:
            st.metric("Passed", pass_count, delta=f"{(pass_count/len(df)*100):.1f}%")

        with stat_col3:
            st.metric("Failed", fail_count, delta=f"-{(fail_count/len(df)*100):.1f}%", delta_color="inverse")

        with stat_col4:
            pass_rate = (pass_count / len(df)) * 100
            status = "✅ Goed" if pass_rate >= 80 else "⚠️ Aandacht nodig" if pass_rate >= 60 else "❌ Kritiek"
            st.metric("Status", status)

        st.markdown("---")

        # Failed requirements
        st.markdown(f"### ❌ Gefaalde Requirements ({fail_count})")

        if fail_count == 0:
            st.success(f"🎉 Alle requirements voldoen aan het '{criterion_info['name']}' criterium!")
        else:
            failed_df = get_failed_requirements_for_criterion(df, selected_criterion)

            # Sort by quality score
            failed_df_sorted = failed_df.sort_values('quality_score')

            for idx, row in failed_df_sorted.iterrows():
                with st.expander(f"{row['id']} - Score: {int(row['quality_score'])}/8"):
                    st.markdown(f"**Label:** {row['label']}")
                    st.markdown(f"**Quality Score:** {int(row['quality_score'])}/8")

                    justification_col = f"{selected_criterion}_justification"
                    if justification_col in row and pd.notna(row[justification_col]):
                        st.markdown("#### Waarom gefaald?")
                        st.warning(row[justification_col])

                    if 'suggestion' in row and pd.notna(row['suggestion']):
                        st.markdown("#### 💡 Suggestie")
                        st.info(row['suggestion'])

                    if 'full_text' in row and pd.notna(row['full_text']):
                        with st.expander("📄 Volledige tekst"):
                            st.text(row['full_text'])

# Tab 3: Custom Requirements Input
with tab3:
    st.markdown("### ✍️ Handmatige Requirement Invoer")
    st.markdown("Voer zelf requirements in of upload ze via CSV/Excel")

    # Initialize custom requirements in session state
    if 'custom_requirements' not in st.session_state:
        st.session_state['custom_requirements'] = []

    # Initialize counter for auto-generated IDs
    if 'custom_req_counter' not in st.session_state:
        st.session_state['custom_req_counter'] = 1

    # Sub-tabs for input methods
    subtab1, subtab2, subtab3 = st.tabs(["📝 Enkele Requirement", "📊 Bulk Import", "👀 Beheer"])

    # Subtab 1: Single requirement input
    with subtab1:
        st.markdown("#### Voeg een nieuwe requirement toe")

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
                    help="ID van parent requirement (optioneel)",
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

    # Subtab 2: Bulk import
    with subtab2:
        st.markdown("#### 📊 Bulk Import via CSV/Excel")

        # Download template
        col1, col2 = st.columns(2)

        with col1:
            # Create CSV template
            template_df = pd.DataFrame({
                'id': ['CUSTOM-001', 'CUSTOM-002', 'CUSTOM-003'],
                'label': ['Example 1', 'Example 2', 'Example 3'],
                'text': [
                    'Het systeem moet binnen 2 seconden reageren...',
                    'De applicatie moet voldoen aan GDPR wetgeving...',
                    'Alle gebruikersdata moet encrypted worden opgeslagen...'
                ],
                'parent_id': ['', 'CUSTOM-001', 'CUSTOM-001'],
                'parent_text': ['', 'Parent tekst...', 'Parent tekst...']
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
        uploaded_file = st.file_uploader(
            "Upload ingevuld bestand",
            type=['csv', 'xlsx'],
            help="Upload een bestand met requirements"
        )

        if uploaded_file:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df_upload = pd.read_csv(uploaded_file)
                else:
                    df_upload = pd.read_excel(uploaded_file)

                # Validate columns
                required_cols = ['id', 'text']
                if not all(col in df_upload.columns for col in required_cols):
                    st.error(f"❌ Bestand moet tenminste deze kolommen bevatten: {', '.join(required_cols)}")
                else:
                    st.success(f"✅ Bestand geladen: {len(df_upload)} requirements gevonden")

                    # Preview
                    st.dataframe(df_upload.head(10), use_container_width=True)

                    # Import button
                    if st.button("📥 Importeer Requirements", type="primary"):
                        imported_count = 0
                        duplicate_count = 0
                        error_count = 0

                        existing_ids = [r['id'] for r in st.session_state['custom_requirements']]

                        for idx, row in df_upload.iterrows():
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

    # Subtab 3: Management
    with subtab3:
        st.markdown("#### 👀 Huidige Custom Requirements")

        if not st.session_state['custom_requirements']:
            st.info("📭 Nog geen custom requirements toegevoegd.")
        else:
            # Statistics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Totaal", len(st.session_state['custom_requirements']))

            with col2:
                with_parent = sum(1 for r in st.session_state['custom_requirements'] if r['parent_id'])
                st.metric("Met Parent", with_parent)

            with col3:
                manual_count = sum(1 for r in st.session_state['custom_requirements'] if r.get('source') == 'manual')
                st.metric("Handmatig", manual_count)

            st.markdown("---")

            # Display requirements
            for idx, req in enumerate(st.session_state['custom_requirements']):
                with st.expander(f"{req['id']} - {req['label'][:50]}..."):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"**ID:** {req['id']}")
                        st.markdown(f"**Label:** {req['label']}")
                        st.markdown(f"**Text:** {req['text']}")
                        if req['parent_id']:
                            st.markdown(f"**Parent ID:** {req['parent_id']}")
                        st.markdown(f"**Bron:** {req.get('source', 'unknown')}")

                    with col2:
                        if st.button("🗑️ Verwijder", key=f"delete_{idx}"):
                            st.session_state['custom_requirements'].pop(idx)
                            st.rerun()

            st.markdown("---")

            # Export and clear
            col1, col2, col3 = st.columns(3)

            with col1:
                # CSV export
                df_export = pd.DataFrame(st.session_state['custom_requirements'])
                csv_export = df_export.to_csv(index=False)

                st.download_button(
                    "📥 Download CSV",
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
                    "📥 Download Excel",
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

    st.markdown("---")
    st.markdown("### 🔗 Integratie met RDF Requirements")

    merge_option = st.radio(
        "Hoe wil je custom requirements gebruiken?",
        options=["merge_with_rdf", "custom_only", "rdf_only"],
        format_func=lambda x: {
            "merge_with_rdf": "📎 Merge - Combineer custom + RDF requirements",
            "custom_only": "✍️ Custom Only - Gebruik alleen custom requirements",
            "rdf_only": "📤 RDF Only - Gebruik alleen RDF requirements"
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

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 Criteria Navigatie")

    # Show criteria list if analysis results exist
    if st.session_state.get(SESSION_KEYS['analysis_results']) is not None:
        for criterion in CRITERIA_ORDER:
            info = CRITERIA[criterion]
            if st.button(f"{info['icon']} {info['name_nl']}", key=f"nav_{criterion}", use_container_width=True):
                st.rerun()

    st.markdown("---")

    # Custom requirements status
    st.markdown("### ✍️ Custom Requirements")

    custom_count = len(st.session_state.get('custom_requirements', []))
    if custom_count > 0:
        st.success(f"✅ {custom_count} custom requirement(s)")
    else:
        st.info("⏳ Geen custom requirements")

    merge_mode = st.session_state.get('requirement_merge_mode', 'merge_with_rdf')
    mode_display = {
        "merge_with_rdf": "📎 Merge Mode",
        "custom_only": "✍️ Custom Only",
        "rdf_only": "📤 RDF Only"
    }
    st.info(f"**Mode:** {mode_display[merge_mode]}")
