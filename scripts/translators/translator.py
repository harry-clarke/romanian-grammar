from typing import Dict, List

from scripts.part_of_speech import PartOfSpeech

TermTranslations = List[str]
Translations = Dict[PartOfSpeech, TermTranslations]


class Translator:
    def get_translations(self, from_language: str, to_language: str, word: str) -> Translations:
        raise NotImplementedError()
