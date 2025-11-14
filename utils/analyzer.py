"""
ISO/IEC/IEEE 29148 Requirements Analyzer
Uses Azure OpenAI to analyze requirements quality based on international standards
"""

import json
import logging
import concurrent.futures
from typing import List, Dict, Optional
from openai import AzureOpenAI
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class RequirementsAnalyzer:
    """
    Analyzer class for ISO/IEC/IEEE 29148 requirements quality assessment.
    """

    def __init__(
        self,
        azure_endpoint: str,
        api_key: str,
        api_version: str = "2024-12-01-preview",
        model_name: str = "o3-mini-1",
        batch_size: int = 5,
        max_completion_tokens: int = 10000,
        concurrent_workers: int = 15
    ):
        """
        Initialize the analyzer with Azure OpenAI credentials.

        Args:
            azure_endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: API version
            model_name: Model deployment name
            batch_size: Number of requirements per batch
            max_completion_tokens: Max tokens for completion
            concurrent_workers: Number of parallel workers
        """
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_completion_tokens = max_completion_tokens
        self.concurrent_workers = concurrent_workers

        try:
            self.client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version=api_version,
            )
            logging.info("Azure OpenAI client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Azure OpenAI client: {e}")
            self.client = None

    def analyze_batch_with_llm(self, batch: List[Dict]) -> List[Dict]:
        """
        Sends a batch of requirements to the LLM for ISO/IEC/IEEE 29148 quality analysis.

        Args:
            batch: List of requirement dictionaries with 'id', 'text', and optional 'parent_context'

        Returns:
            List of analysis results with quality scores and justifications
        """
        if not self.client:
            logging.error("API client is not initialized. Skipping analysis.")
            return []

        system_prompt = """
        U bent een expert in requirements engineering en systems engineering, gespecialiseerd in het analyseren van eisen volgens de ISO/IEC/IEEE 29148 standaard en de INCOSE Guide to Writing Requirements (GtWR, Rev 4, 2023).
        Uw taak is om een lijst met eisen te analyseren op basis van de kwaliteitscriteria zoals gedefinieerd in ISO/IEC/IEEE 29148. 
        Daarnaast moet u bij elke beoordeling en motivatie expliciet gebruikmaken van de richtlijnen, kenmerken (C1–C15) en schrijfregels uit de INCOSE GtWR. 
        Gebruik de INCOSE-criteria uitsluitend als verdieping van uw analyse en motivatie, maar wijzig de structuur van de uiteindelijke beoordeling NIET: u blijft uitsluitend de acht ISO/IEC/IEEE 29148 criteria beoordelen.

        Voor elke eis krijgt u de specifieke tekst en, indien beschikbaar, de tekst van de overkoepelende 'oudereis' voor context. Baseer uw analyse op de specifieke eis, maar gebruik de oudereis om de relevantie en het doel beter te begrijpen.

        ### Gebruik INCOSE bij uw redenering
        Wanneer u de acht ISO/IEC/IEEE 29148 criteria beoordeelt, moet u indien relevant verwijzen naar:
        - INCOSE-kenmerken zoals:
        - C1 Necessary
        - C2 Appropriate
        - C3 Unambiguous
        - C4 Complete
        - C5 Singular
        - C6 Feasible
        - C7 Verifiable / Validatable
        - C8 Correctness
        - C12 Consistent (geen conflicten)
        - INCOSE-regels voor eisen, zoals:
        - vermijden van ambiguïteit en vaag taalgebruik
        - eisen moeten exact één verplichting bevatten (“shall”)
        - implementatievrij (“wat” i.p.v. “hoe”)
        - eisen moeten verifieerbaar zijn (measurable success criteria afleidbaar)
        - eisen moeten correct, traceerbaar en passend binnen het juiste hiërarchische niveau zijn
        - gebruik van requirement patterns (Appendix C) wanneer relevant
        - rationale en attributen als hulpmiddel om interpretatieruimte te voorkomen

        Gebruik deze INCOSE-richtlijnen expliciet om uw Nederlandse toelichtingen, rechtvaardigingen en verbeteradviezen te onderbouwen. 
        Maar wijzig de ISO-criteria niet en voeg geen nieuwe beoordelingsvelden toe.

        ### De acht ISO/IEC/IEEE 29148 kwaliteitscriteria:
        1. NECESSARY (Noodzakelijk)
        2. UNAMBIGUOUS (Eenduidig)
        3. COMPLETE (Compleet)
        4. SINGULAR (Enkelvoudig)
        5. FEASIBLE (Haalbaar)
        6. VERIFIABLE (Verifieerbaar)
        7. TRACEABLE (Traceerbaar)
        8. IMPLEMENTATION_FREE (Implementatie-onafhankelijk)

        De input is in het Nederlands en uw volledige output, inclusief alle rechtvaardigingen en suggesties, moet ook in het Nederlands zijn.

        ### VERPLICHT JSON-FORMAAT
        Uw antwoord MOET een enkel, geldig JSON-object zijn dat één sleutel bevat: "results".  
        Elk element in deze lijst moet een woordenboek zijn met exact de volgende sleutels:

        - "id"
        - "necessary" (boolean)
        - "necessary_justification" (string)
        - "unambiguous" (boolean)
        - "unambiguous_justification" (string)
        - "complete" (boolean)
        - "complete_justification" (string)
        - "singular" (boolean)
        - "singular_justification" (string)
        - "feasible" (boolean)
        - "feasible_justification" (string)
        - "verifiable" (boolean)
        - "verifiable_justification" (string)
        - "traceable" (boolean)
        - "traceable_justification" (string)
        - "implementation_free" (boolean)
        - "implementation_free_justification" (string)
        - "quality_score" (integer 0–8)
        - "suggestion" (string met verbeteradvies volgens ISO + INCOSE)

        Lever GEEN tekst buiten deze JSON-structuur.
        """

        user_prompt = json.dumps(batch, ensure_ascii=False, indent=2)

        try:
            logging.info(f"Sending a batch of {len(batch)} requirements for ISO/IEC/IEEE 29148 analysis...")

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_completion_tokens=self.max_completion_tokens,
                response_format={"type": "json_object"}
            )

            response_content = response.choices[0].message.content
            results_json = json.loads(response_content)

            if "results" in results_json and isinstance(results_json["results"], list):
                batch_results = results_json["results"]
                logging.info(f"Batch processed successfully. Received {len(batch_results)} analyses.")
                return batch_results
            else:
                logging.error("JSON response did not contain the expected 'results' list.")
                logging.error(f"Raw response received: {response_content}")
                return []

        except json.JSONDecodeError as json_err:
            logging.error(f"JSON decoding failed: {json_err}")
            return []
        except Exception as e:
            logging.error(f"An error occurred during the OpenAI API call: {e}")
            return []

    def process_single_batch(self, batch_data: tuple) -> List[Dict]:
        """
        Processes a single batch of requirements, including parent context in the prompt.

        Args:
            batch_data: Tuple of (batch_index, batch_requirements_list)

        Returns:
            List of processed analysis results
        """
        batch_index, batch = batch_data
        logging.info(f"Worker starting on batch {batch_index}...")

        original_req_map = {req['id']: req for req in batch}

        # Create a detailed prompt object with parent context
        prompt_batch = []
        for req in batch:
            prompt_item = {"id": req["id"], "text": req["text"]}
            if req.get("parent_text"):
                prompt_item["parent_context"] = req["parent_text"]
            prompt_batch.append(prompt_item)

        batch_results = self.analyze_batch_with_llm(prompt_batch)

        processed_analyses = []
        if batch_results:
            for analysis in batch_results:
                req_id = analysis.get('id')
                original_req = original_req_map.get(req_id)
                if original_req:
                    analysis['label'] = original_req['label']
                    analysis['full_text'] = original_req['text']
                    analysis['parent_id'] = original_req.get('parent_id')
                    processed_analyses.append(analysis)
                else:
                    logging.warning(f"Received analysis for an unknown ID '{req_id}' in batch {batch_index}.")
        else:
            logging.warning(f"Batch {batch_index} returned no valid results.")
            for req in batch:
                processed_analyses.append({
                    'id': req['id'],
                    'label': req['label'],
                    'full_text': req['text'],
                    'parent_id': req.get('parent_id'),
                    'quality_score': 0,
                    'suggestion': 'ERROR: Failed to get analysis from LLM.'
                })

        return processed_analyses

    def analyze_requirements(
        self,
        requirements: List[Dict],
        max_requirements: Optional[int] = None,
        progress_callback=None
    ) -> List[Dict]:
        """
        Analyzes a list of requirements using parallel batch processing.

        Args:
            requirements: List of requirement dictionaries
            max_requirements: Optional limit on number of requirements to analyze
            progress_callback: Optional callback function for progress updates

        Returns:
            List of analysis results
        """
        logging.info("--- STARTING CONCURRENT ISO/IEC/IEEE 29148 ANALYSIS ---")

        if not requirements:
            logging.error("No requirements provided for analysis.")
            return []

        # Apply analysis limit if specified
        requirements_to_process = requirements
        if max_requirements is not None and max_requirements > 0:
            logging.info(f"Limiting analysis to the first {max_requirements} requirements.")
            requirements_to_process = requirements[:max_requirements]

        # Create batches
        batches = [
            (i // self.batch_size + 1, requirements_to_process[i:i + self.batch_size])
            for i in range(0, len(requirements_to_process), self.batch_size)
        ]

        all_analyses = []
        logging.info(f"Starting analysis with {self.concurrent_workers} workers for {len(requirements_to_process)} requirements.")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrent_workers) as executor:
            if progress_callback:
                # Use custom progress callback
                futures = {executor.submit(self.process_single_batch, batch): batch[0] for batch in batches}
                for future in concurrent.futures.as_completed(futures):
                    batch_idx = futures[future]
                    result = future.result()
                    all_analyses.extend(result)
                    progress_callback(batch_idx, len(batches))
            else:
                # Use tqdm progress bar
                results_iterator = list(tqdm(
                    executor.map(self.process_single_batch, batches),
                    total=len(batches),
                    desc="Analyzing batches"
                ))
                for result_list in results_iterator:
                    all_analyses.extend(result_list)

        logging.info(f"Analysis complete. Processed {len(all_analyses)} requirements.")
        return all_analyses
