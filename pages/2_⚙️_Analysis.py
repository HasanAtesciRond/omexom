"""
Analysis Progress Page
Starts and monitors the ISO 29148 requirements analysis
"""

import streamlit as st
import pandas as pd
import time
from utils.analyzer import RequirementsAnalyzer
from config.settings import SESSION_KEYS

st.set_page_config(page_title="Run Analysis", page_icon="⚙️", layout="wide")

st.title("⚙️ ISO 29148 Analyse")
st.markdown("Start de requirements quality analyse met Azure OpenAI")

# Get merge mode and prepare requirements
merge_mode = st.session_state.get('requirement_merge_mode', 'merge_with_rdf')
rdf_requirements = st.session_state.get(SESSION_KEYS['requirements'], []) or []
custom_requirements = st.session_state.get('custom_requirements', [])

# Prepare requirements based on merge mode
if merge_mode == "merge_with_rdf":
    # Add source indicator to RDF requirements if not present
    for req in rdf_requirements:
        if 'source' not in req:
            req['source'] = 'rdf'

    # Combine both sources
    requirements = rdf_requirements + custom_requirements

    if not requirements:
        st.warning("⚠️ Geen requirements gevonden. Upload een RDF bestand of voeg custom requirements toe.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➡️ Naar Upload Pagina"):
                st.switch_page("pages/1_📤_Upload.py")
        with col2:
            if st.button("➡️ Naar Criteria & Custom Requirements"):
                st.switch_page("pages/5_🔍_Criteria.py")
        st.stop()

    st.info(f"📎 **Merge Mode:** {len(rdf_requirements)} RDF + {len(custom_requirements)} Custom = **{len(requirements)} totaal**")

elif merge_mode == "custom_only":
    requirements = custom_requirements

    if not requirements:
        st.warning("⚠️ Geen custom requirements gevonden. Voeg custom requirements toe op de Manual Input pagina.")
        if st.button("➡️ Naar Criteria & Custom Requirements"):
            st.switch_page("pages/5_🔍_Criteria.py")
        st.stop()

    st.info(f"✍️ **Custom Only Mode:** {len(requirements)} custom requirements")

else:  # rdf_only
    # Add source indicator to RDF requirements
    for req in rdf_requirements:
        if 'source' not in req:
            req['source'] = 'rdf'

    requirements = rdf_requirements

    if not requirements:
        st.warning("⚠️ Geen RDF requirements gevonden. Upload eerst een bestand op de Upload pagina.")
        if st.button("➡️ Naar Upload Pagina"):
            st.switch_page("pages/1_📤_Upload.py")
        st.stop()

    st.info(f"📤 **RDF Only Mode:** {len(requirements)} RDF requirements")
config = st.session_state[SESSION_KEYS['analyzer_config']]

# Check if API is configured
if not config['azure_endpoint'] or not config['api_key']:
    st.error("❌ Azure OpenAI niet geconfigureerd")
    st.info("Configureer de Azure OpenAI credentials in de sidebar van de homepage.")
    st.stop()

# Analysis configuration summary
st.markdown("### 📋 Analyse Configuratie")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_reqs = len(requirements)
    max_reqs = st.session_state.get('max_requirements_to_analyze')
    if max_reqs:
        st.metric("Te analyseren", f"{max_reqs} van {total_reqs}")
    else:
        st.metric("Te analyseren", total_reqs)

with col2:
    st.metric("Batch Size", config['batch_size'])

with col3:
    st.metric("Workers", config['concurrent_workers'])

with col4:
    estimated_time = (max_reqs or total_reqs) * 2 / 60  # Rough estimate: 2 sec per req
    st.metric("Geschatte tijd", f"~{estimated_time:.1f} min")

st.markdown("---")

# Show criteria mode status
use_custom_criteria = st.session_state.get('use_custom_criteria', False)

if use_custom_criteria:
    custom_criteria_count = len(st.session_state.get('custom_criteria', []))
    if custom_criteria_count > 0:
        st.success(f"🎨 **Custom Criteria Mode Actief** - {custom_criteria_count} custom criteria zullen worden gebruikt")
    else:
        st.warning("⚠️ Custom criteria mode is ingeschakeld maar geen criteria gedefinieerd - standaard ISO 29148 wordt gebruikt")
else:
    st.info("📋 **Standaard Mode** - ISO/IEC/IEEE 29148 criteria worden gebruikt (8 criteria)")

st.markdown("---")

# Start analysis button
if not st.session_state.get(SESSION_KEYS['analysis_in_progress'], False):
    st.markdown("### 🚀 Start Analyse")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Start ISO 29148 Analyse", type="primary", use_container_width=True):
            st.session_state[SESSION_KEYS['analysis_in_progress']] = True
            st.rerun()
else:
    # Analysis is running
    st.markdown("### ⏳ Analyse Bezig...")

    # Check if custom criteria are enabled
    use_custom_criteria = st.session_state.get('use_custom_criteria', False)
    custom_prompt = None

    if use_custom_criteria:
        # Use custom generated prompt if available
        custom_prompt = st.session_state.get('generated_custom_prompt')

        if not custom_prompt:
            # Generate it on the fly if not already generated
            custom_criteria = st.session_state.get('custom_criteria', [])

            if custom_criteria:
                st.info("🤖 Custom criteria gedetecteerd - genereer aangepaste prompt...")

                from utils.prompt_generator import PromptGenerator

                try:
                    generator = PromptGenerator(
                        azure_endpoint=config['azure_endpoint'],
                        api_key=config['api_key'],
                        api_version=config['api_version'],
                        model_name=config['model_name']
                    )

                    custom_prompt = generator.generate_custom_prompt(custom_criteria)
                    st.session_state['generated_custom_prompt'] = custom_prompt
                    st.success("✅ Aangepaste prompt gegenereerd!")

                except Exception as e:
                    st.error(f"❌ Fout bij genereren custom prompt: {str(e)}")
                    st.warning("⚠️ Terugvallen op standaard ISO 29148 prompt...")
                    use_custom_criteria = False
            else:
                st.warning("⚠️ Custom criteria ingeschakeld maar geen criteria gedefinieerd. Gebruik standaard ISO 29148 criteria.")
                use_custom_criteria = False

    # Show which criteria mode is being used
    if use_custom_criteria and custom_prompt:
        st.success(f"🎨 **Criteria Mode:** Custom Criteria ({len(st.session_state.get('custom_criteria', []))} criteria)")
    else:
        st.info("📋 **Criteria Mode:** ISO/IEC/IEEE 29148 (8 standaard criteria)")

    # Create analyzer with optional custom prompt
    analyzer = RequirementsAnalyzer(
        azure_endpoint=config['azure_endpoint'],
        api_key=config['api_key'],
        api_version=config['api_version'],
        model_name=config['model_name'],
        batch_size=config['batch_size'],
        max_completion_tokens=config['max_completion_tokens'],
        concurrent_workers=config['concurrent_workers'],
        custom_system_prompt=custom_prompt if use_custom_criteria else None
    )

    # Progress containers
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.expander("📋 Analyse Log", expanded=False)

    # Start analysis
    max_reqs_to_analyze = st.session_state.get('max_requirements_to_analyze')

    try:
        with log_container:
            st.text("🔄 Analyse gestart...")
            start_time = time.time()

        # Custom progress callback
        def update_progress(batch_idx, total_batches):
            progress = batch_idx / total_batches
            progress_bar.progress(progress)
            status_text.text(f"Batch {batch_idx}/{total_batches} verwerkt ({progress*100:.1f}%)")

            elapsed = time.time() - start_time
            est_total = elapsed / progress if progress > 0 else 0
            remaining = est_total - elapsed

            with log_container:
                st.text(f"⏱️ Verstreken tijd: {elapsed/60:.1f} min | Resterend: ~{remaining/60:.1f} min")

        # Run analysis
        results = analyzer.analyze_requirements(
            requirements=requirements,
            max_requirements=max_reqs_to_analyze,
            progress_callback=update_progress
        )

        if results:
            # Convert to DataFrame
            df = pd.DataFrame(results)

            # Store in session state
            st.session_state[SESSION_KEYS['analysis_results']] = df
            st.session_state[SESSION_KEYS['analysis_in_progress']] = False

            # Success
            progress_bar.progress(1.0)
            status_text.empty()

            end_time = time.time()
            duration = (end_time - start_time) / 60

            st.success(f"✅ Analyse voltooid! {len(results)} requirements geanalyseerd in {duration:.1f} minuten")

            with log_container:
                st.text(f"✅ Analyse succesvol afgerond")
                st.text(f"📊 {len(results)} requirements geanalyseerd")
                st.text(f"⏱️ Totale tijd: {duration:.1f} minuten")

            # Show quick summary
            st.markdown("### 📊 Snelle Samenvatting")

            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

            with summary_col1:
                avg_score = df['quality_score'].mean()
                st.metric("Gemiddelde Score", f"{avg_score:.2f}/8")

            with summary_col2:
                excellent_count = len(df[df['quality_score'] >= 7])
                st.metric("Excellent (7-8)", excellent_count)

            with summary_col3:
                poor_count = len(df[df['quality_score'] < 3])
                st.metric("Poor (0-2)", poor_count)

            with summary_col4:
                pass_rate = (df['necessary'].sum() / len(df)) * 100
                st.metric("Necessary Pass %", f"{pass_rate:.1f}%")

            # Next steps
            st.markdown("---")
            st.markdown("### ✅ Volgende Stap")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success("✅ Analyse voltooid! Bekijk de resultaten in het Dashboard.")

                if st.button("➡️ Naar Dashboard", type="primary", use_container_width=True, key="goto_dashboard"):
                    # Ensure analysis_in_progress is False before navigation
                    st.session_state[SESSION_KEYS['analysis_in_progress']] = False
                    st.switch_page("pages/3_📊_Dashboard.py")

        else:
            st.error("❌ Analyse mislukt. Geen resultaten ontvangen.")
            st.session_state[SESSION_KEYS['analysis_in_progress']] = False

            with log_container:
                st.text("❌ Analyse mislukt - controleer de logs en API configuratie")

    except Exception as e:
        st.error(f"❌ Fout tijdens analyse: {str(e)}")
        st.session_state[SESSION_KEYS['analysis_in_progress']] = False

        with log_container:
            st.text(f"❌ Error: {str(e)}")

        if st.button("🔄 Probeer opnieuw"):
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Analyse Status")

    if st.session_state.get(SESSION_KEYS['analysis_results']) is not None:
        df = st.session_state[SESSION_KEYS['analysis_results']]
        st.success(f"✅ {len(df)} requirements geanalyseerd")

        st.markdown("#### 📊 Quick Stats")
        st.metric("Avg Score", f"{df['quality_score'].mean():.2f}")
        st.metric("Min Score", int(df['quality_score'].min()))
        st.metric("Max Score", int(df['quality_score'].max()))
    else:
        st.warning("⏳ Nog niet geanalyseerd")

    st.markdown("---")

    if st.session_state.get(SESSION_KEYS['analysis_in_progress'], False):
        if st.button("⏸️ Annuleer Analyse", type="secondary"):
            st.session_state[SESSION_KEYS['analysis_in_progress']] = False
            st.warning("Analyse geannuleerd")
            st.rerun()
