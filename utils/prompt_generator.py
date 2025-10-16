"""
Prompt Generator for Custom Criteria
Uses LLM to adapt the system prompt based on user-defined custom criteria
"""

import json
import logging
from typing import List, Dict, Optional
from openai import AzureOpenAI


class PromptGenerator:
    """
    Generates custom analysis prompts based on user-defined criteria using LLM.
    """

    def __init__(self, azure_endpoint: str, api_key: str, api_version: str = "2024-12-01-preview", model_name: str = "o3-mini-1"):
        """
        Initialize the prompt generator.

        Args:
            azure_endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: API version
            model_name: Model deployment name
        """
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.model_name = model_name

        try:
            self.client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version=api_version,
            )
            logging.info("PromptGenerator: Azure OpenAI client initialized successfully.")
        except Exception as e:
            logging.error(f"PromptGenerator: Failed to initialize Azure OpenAI client: {e}")
            self.client = None

    def generate_custom_prompt(self, custom_criteria: List[Dict]) -> str:
        """
        Generate a custom analysis prompt based on user-defined criteria.

        Args:
            custom_criteria: List of custom criteria dictionaries with:
                - name: Criterion name (e.g., "Security")
                - description: What the criterion evaluates
                - guidance: How to evaluate (optional)

        Returns:
            Generated system prompt string for requirements analysis
        """
        if not self.client:
            logging.error("PromptGenerator: API client not initialized. Returning default prompt.")
            return self._get_default_prompt()

        if not custom_criteria or len(custom_criteria) == 0:
            logging.info("PromptGenerator: No custom criteria provided. Using default ISO 29148 prompt.")
            return self._get_default_prompt()

        # Create meta-prompt for the LLM to generate the analysis prompt
        meta_prompt = f"""
Je bent een expert in requirements engineering en prompt engineering.

Je taak is om een **gedetailleerde system prompt** te genereren voor een LLM die requirements gaat analyseren.
De gebruiker heeft de volgende {len(custom_criteria)} custom kwaliteitscriteria gedefinieerd:

{self._format_criteria_for_meta_prompt(custom_criteria)}

BELANGRIJKE INSTRUCTIES:
1. Genereer een volledige system prompt in het Nederlands die de LLM instrueert om requirements te analyseren op basis van deze custom criteria
2. De prompt moet dezelfde structuur volgen als de ISO/IEC/IEEE 29148 prompt (zie voorbeeld hieronder)
3. Voor elk criterium moet de LLM een boolean (true/false) en justification geven
4. Voeg een quality_score toe (0-{len(custom_criteria)} op basis van hoeveel criteria voldaan zijn)
5. Voeg een suggestion field toe voor verbeteringsvoorstellen

STRUCTUUR VAN DE OUTPUT PROMPT:
- Begin met: "U bent een expert in requirements engineering..."
- Leg uit dat de taak is om requirements te analyseren op basis van custom criteria
- List alle {len(custom_criteria)} criteria genummerd met hun beschrijving
- Specificeer dat de output JSON moet zijn met deze velden:
  * "id": requirement ID
  * Voor elk criterium: "{{criterion_key}}": boolean en "{{criterion_key}}_justification": string
  * "quality_score": integer 0-{len(custom_criteria)}
  * "suggestion": improvement suggestion in Dutch

VOORBEELD ISO 29148 PROMPT TER REFERENTIE:
```
U bent een expert in requirements engineering en systems engineering, gespecialiseerd in het analyseren van eisen volgens de ISO/IEC/IEEE 29148 standaard.

Uw taak is om een lijst met eisen te analyseren op basis van de kwaliteitscriteria zoals gedefinieerd in ISO/IEC/IEEE 29148.
Voor elke eis krijgt u de specifieke tekst en, indien beschikbaar, de tekst van de overkoepelende 'oudereis' voor context.

Evalueer elke eis op de volgende kwaliteitscriteria:

1. CRITERIUM_NAAM: [beschrijving]
2. CRITERIUM_NAAM: [beschrijving]
...

Uw antwoord MOET een enkel, geldig JSON-object zijn dat één sleutel bevat, "results", die een lijst met woordenboeken bevat.
Elk woordenboek moet overeenkomen met een input-eis en de volgende sleutels bevatten:
- "id": requirement ID
- "criterium_key": boolean
- "criterium_key_justification": string in Nederlands
...
- "quality_score": 0-N
- "suggestion": string in Nederlands

Lever geen tekst of uitleg buiten deze JSON-structuur.
```

Genereer NU de volledige custom system prompt. Geef ALLEEN de prompt terug, geen uitleg ervoor of erna.
"""

        try:
            logging.info(f"PromptGenerator: Generating custom prompt for {len(custom_criteria)} criteria...")

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": meta_prompt}
                ],
                max_completion_tokens=4000,
                temperature=0.3  # Lower temperature for more consistent prompt generation
            )

            generated_prompt = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if generated_prompt.startswith("```"):
                lines = generated_prompt.split("\n")
                generated_prompt = "\n".join(lines[1:-1]) if len(lines) > 2 else generated_prompt

            logging.info("PromptGenerator: Custom prompt generated successfully.")
            logging.debug(f"Generated prompt:\n{generated_prompt}")

            return generated_prompt

        except Exception as e:
            logging.error(f"PromptGenerator: Failed to generate custom prompt: {e}")
            return self._get_default_prompt()

    def _format_criteria_for_meta_prompt(self, criteria: List[Dict]) -> str:
        """Format criteria list for inclusion in meta-prompt."""
        formatted = []
        for idx, criterion in enumerate(criteria, 1):
            formatted.append(f"{idx}. **{criterion['name']}**")
            formatted.append(f"   - Beschrijving: {criterion.get('description', 'Geen beschrijving')}")
            if criterion.get('guidance'):
                formatted.append(f"   - Guidance: {criterion['guidance']}")
            formatted.append("")
        return "\n".join(formatted)

    def _get_default_prompt(self) -> str:
        """Return the default ISO/IEC/IEEE 29148 prompt."""
        return """
U bent een expert in requirements engineering en systems engineering, gespecialiseerd in het analyseren van eisen volgens de ISO/IEC/IEEE 29148 standaard.

Uw taak is om een lijst met eisen te analyseren op basis van de kwaliteitscriteria zoals gedefinieerd in ISO/IEC/IEEE 29148.
Voor elke eis krijgt u de specifieke tekst en, indien beschikbaar, de tekst van de overkoepelende 'oudereis' voor context.
Baseer uw analyse op de specifieke eis, maar gebruik de oudereis om de relevantie en het doel beter te begrijpen.

Evalueer elke eis op de volgende ISO/IEC/IEEE 29148 kwaliteitscriteria:

1. NECESSARY (Noodzakelijk): Is de eis noodzakelijk en voegt deze waarde toe aan het systeem?
2. UNAMBIGUOUS (Eenduidig): Is de eis duidelijk geformuleerd zonder ruimte voor meerdere interpretaties?
3. COMPLETE (Compleet): Bevat de eis alle noodzakelijke informatie zonder TBD's of open punten?
4. SINGULAR (Enkelvoudig): Beschrijft de eis slechts één specifieke eis (geen 'en/of' constructies)?
5. FEASIBLE (Haalbaar): Is de eis technisch en economisch realiseerbaar binnen de context?
6. VERIFIABLE (Verifieerbaar): Kan de eis objectief getest of geverifieerd worden?
7. TRACEABLE (Traceerbaar): Is de eis identificeerbaar en traceerbaar?
8. IMPLEMENTATION_FREE (Implementatie-onafhankelijk): Beschrijft de eis WAT er nodig is, niet HOE het moet worden geïmplementeerd?

De input is in het Nederlands en uw volledige output, inclusief alle rechtvaardigingen en suggesties, moet ook in het Nederlands zijn.

Uw antwoord MOET een enkel, geldig JSON-object zijn dat één sleutel bevat, "results", die een lijst met woordenboeken bevat.
Elk woordenboek moet overeenkomen met een input-eis en de volgende Engelse sleutels bevatten:
- "id": De identificatiecode van de specifieke eis.
- "necessary": Een boolean (true/false).
- "necessary_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "unambiguous": Een boolean (true/false).
- "unambiguous_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "complete": Een boolean (true/false).
- "complete_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "singular": Een boolean (true/false).
- "singular_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "feasible": Een boolean (true/false).
- "feasible_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "verifiable": Een boolean (true/false).
- "verifiable_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "traceable": Een boolean (true/false).
- "traceable_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "implementation_free": Een boolean (true/false).
- "implementation_free_justification": Een string in het Nederlands die uw beslissing uitlegt.
- "quality_score": Een geheel getal van 0 tot 8 (aantal criteria dat wordt voldaan).
- "suggestion": Een string in het Nederlands met een concreet voorstel om de eis te verbeteren volgens ISO/IEC/IEEE 29148.

Lever geen tekst of uitleg buiten deze JSON-structuur.
"""

    def get_criteria_keys_from_prompt(self, custom_criteria: List[Dict]) -> List[str]:
        """
        Extract criterion keys that will be used in the analysis results.

        Args:
            custom_criteria: List of custom criteria

        Returns:
            List of criterion keys (lowercase, underscored)
        """
        if not custom_criteria:
            return ['necessary', 'unambiguous', 'complete', 'singular',
                    'feasible', 'verifiable', 'traceable', 'implementation_free']

        # Convert criterion names to keys (lowercase, replace spaces with underscores)
        keys = []
        for criterion in custom_criteria:
            key = criterion['name'].lower().replace(' ', '_').replace('-', '_')
            # Remove special characters
            key = ''.join(c for c in key if c.isalnum() or c == '_')
            keys.append(key)

        return keys
