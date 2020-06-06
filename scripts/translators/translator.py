from typing import Dict, List

from scripts.part_of_speech import PartOfSpeech

TermTranslations = Dict[str, List[str]]
"""
    A mapping of a suggested starting term to its potential translations.
    Example: get_translations('english', 'romanian', 'be') -> {...: {'to be': 'a fi'}}
"""
Translations = Dict[PartOfSpeech, TermTranslations]


class Translator:
    def get_translations(self, from_language: str, to_language: str, word: str) -> Translations:
        raise NotImplementedError()
