"""
ISO/IEC/IEEE 29148 Criteria Definitions
Provides detailed descriptions and guidance for each quality criterion
"""

CRITERIA = {
    'necessary': {
        'name': 'Necessary',
        'name_nl': 'Noodzakelijk',
        'description': 'The requirement is essential and adds value to the system.',
        'description_nl': 'De eis is essentieel en voegt waarde toe aan het systeem.',
        'guidance': 'Ask: What happens if we remove this requirement? If nothing bad happens, it may not be necessary.',
        'guidance_nl': 'Vraag: Wat gebeurt er als we deze eis verwijderen? Als er niets slechts gebeurt, is het mogelijk niet noodzakelijk.',
        'icon': '✅'
    },
    'unambiguous': {
        'name': 'Unambiguous',
        'name_nl': 'Eenduidig',
        'description': 'The requirement is clearly stated without room for multiple interpretations.',
        'description_nl': 'De eis is duidelijk geformuleerd zonder ruimte voor meerdere interpretaties.',
        'guidance': 'Avoid vague terms like "user-friendly", "fast", "flexible". Use specific, measurable terms.',
        'guidance_nl': 'Vermijd vage termen zoals "gebruiksvriendelijk", "snel", "flexibel". Gebruik specifieke, meetbare termen.',
        'icon': '🎯'
    },
    'complete': {
        'name': 'Complete',
        'name_nl': 'Compleet',
        'description': 'The requirement contains all necessary information without TBDs or open points.',
        'description_nl': 'De eis bevat alle noodzakelijke informatie zonder TBD\'s of open punten.',
        'guidance': 'Check for placeholders, missing details, or references to undefined terms.',
        'guidance_nl': 'Controleer op placeholders, ontbrekende details of verwijzingen naar ongedefinieerde termen.',
        'icon': '📋'
    },
    'singular': {
        'name': 'Singular',
        'name_nl': 'Enkelvoudig',
        'description': 'The requirement describes only one specific requirement (no "and/or" constructions).',
        'description_nl': 'De eis beschrijft slechts één specifieke eis (geen "en/of" constructies).',
        'guidance': 'Split compound requirements connected by "and" or "or" into separate requirements.',
        'guidance_nl': 'Splits samengestelde eisen verbonden door "en" of "of" in afzonderlijke eisen.',
        'icon': '1️⃣'
    },
    'feasible': {
        'name': 'Feasible',
        'name_nl': 'Haalbaar',
        'description': 'The requirement is technically and economically achievable within context.',
        'description_nl': 'De eis is technisch en economisch realiseerbaar binnen de context.',
        'guidance': 'Consider current technology, budget, schedule, and available resources.',
        'guidance_nl': 'Overweeg huidige technologie, budget, planning en beschikbare middelen.',
        'icon': '🔧'
    },
    'verifiable': {
        'name': 'Verifiable',
        'name_nl': 'Verifieerbaar',
        'description': 'The requirement can be objectively tested or verified.',
        'description_nl': 'De eis kan objectief getest of geverifieerd worden.',
        'guidance': 'Ensure there is a clear acceptance criterion or test method.',
        'guidance_nl': 'Zorg ervoor dat er een duidelijk acceptatiecriterium of testmethode is.',
        'icon': '✔️'
    },
    'traceable': {
        'name': 'Traceable',
        'name_nl': 'Traceerbaar',
        'description': 'The requirement is identifiable and traceable throughout the lifecycle.',
        'description_nl': 'De eis is identificeerbaar en traceerbaar gedurende de gehele levenscyclus.',
        'guidance': 'Requirements should have unique identifiers and clear relationships to other requirements.',
        'guidance_nl': 'Eisen moeten unieke identificatoren hebben en duidelijke relaties met andere eisen.',
        'icon': '🔗'
    },
    'implementation_free': {
        'name': 'Implementation-free',
        'name_nl': 'Implementatie-onafhankelijk',
        'description': 'The requirement describes WHAT is needed, not HOW it should be implemented.',
        'description_nl': 'De eis beschrijft WAT er nodig is, niet HOE het moet worden geïmplementeerd.',
        'guidance': 'Focus on desired outcomes and capabilities, not on specific technologies or solutions.',
        'guidance_nl': 'Focus op gewenste resultaten en mogelijkheden, niet op specifieke technologieën of oplossingen.',
        'icon': '🎨'
    }
}

# Ordered list of criteria for consistent display
CRITERIA_ORDER = [
    'necessary',
    'unambiguous',
    'complete',
    'singular',
    'feasible',
    'verifiable',
    'traceable',
    'implementation_free'
]

# Quality score interpretation
SCORE_INTERPRETATION = {
    8: {
        'label': 'Excellent',
        'label_nl': 'Uitstekend',
        'description': 'All ISO 29148 criteria are met. This is a high-quality requirement.',
        'description_nl': 'Alle ISO 29148 criteria zijn voldaan. Dit is een hoogwaardige eis.',
        'color': '#10B981'
    },
    7: {
        'label': 'Very Good',
        'label_nl': 'Zeer Goed',
        'description': '7 out of 8 criteria met. Minor improvements possible.',
        'description_nl': '7 van de 8 criteria voldaan. Kleine verbeteringen mogelijk.',
        'color': '#10B981'
    },
    6: {
        'label': 'Good',
        'label_nl': 'Goed',
        'description': '6 out of 8 criteria met. Some improvements recommended.',
        'description_nl': '6 van de 8 criteria voldaan. Enkele verbeteringen aanbevolen.',
        'color': '#FCD34D'
    },
    5: {
        'label': 'Acceptable',
        'label_nl': 'Acceptabel',
        'description': '5 out of 8 criteria met. Several improvements needed.',
        'description_nl': '5 van de 8 criteria voldaan. Diverse verbeteringen nodig.',
        'color': '#FCD34D'
    },
    4: {
        'label': 'Fair',
        'label_nl': 'Redelijk',
        'description': 'Half of criteria met. Significant improvements needed.',
        'description_nl': 'Helft van de criteria voldaan. Aanzienlijke verbeteringen nodig.',
        'color': '#F59E0B'
    },
    3: {
        'label': 'Poor',
        'label_nl': 'Slecht',
        'description': 'Only 3 criteria met. Major revision required.',
        'description_nl': 'Slechts 3 criteria voldaan. Grote herziening vereist.',
        'color': '#F59E0B'
    },
    2: {
        'label': 'Very Poor',
        'label_nl': 'Zeer Slecht',
        'description': 'Only 2 criteria met. Complete rewrite recommended.',
        'description_nl': 'Slechts 2 criteria voldaan. Volledige herschrijving aanbevolen.',
        'color': '#DC2626'
    },
    1: {
        'label': 'Inadequate',
        'label_nl': 'Onvoldoende',
        'description': 'Only 1 criterion met. Not suitable as a requirement.',
        'description_nl': 'Slechts 1 criterium voldaan. Niet geschikt als eis.',
        'color': '#DC2626'
    },
    0: {
        'label': 'Unacceptable',
        'label_nl': 'Onaanvaardbaar',
        'description': 'No criteria met. This does not qualify as a proper requirement.',
        'description_nl': 'Geen criteria voldaan. Dit kwalificeert niet als een correcte eis.',
        'color': '#DC2626'
    }
}


def get_criterion_info(criterion_key: str, language: str = 'nl') -> dict:
    """
    Get information about a specific criterion.

    Args:
        criterion_key: Key of the criterion (e.g., 'necessary')
        language: Language code ('en' or 'nl')

    Returns:
        Dictionary with criterion information
    """
    if criterion_key not in CRITERIA:
        return {}

    info = CRITERIA[criterion_key].copy()

    if language == 'nl':
        return {
            'name': info['name_nl'],
            'description': info['description_nl'],
            'guidance': info['guidance_nl'],
            'icon': info['icon']
        }
    else:
        return {
            'name': info['name'],
            'description': info['description'],
            'guidance': info['guidance'],
            'icon': info['icon']
        }


def get_score_interpretation(score: int, language: str = 'nl') -> dict:
    """
    Get interpretation for a quality score.

    Args:
        score: Quality score (0-8)
        language: Language code ('en' or 'nl')

    Returns:
        Dictionary with score interpretation
    """
    if score not in SCORE_INTERPRETATION:
        return {}

    info = SCORE_INTERPRETATION[score].copy()

    if language == 'nl':
        return {
            'label': info['label_nl'],
            'description': info['description_nl'],
            'color': info['color']
        }
    else:
        return {
            'label': info['label'],
            'description': info['description'],
            'color': info['color']
        }
