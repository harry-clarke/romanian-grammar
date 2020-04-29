from typing import Dict

from scripts.part_of_speech import PartOfSpeech

PART_OF_SPEECH: Dict[str, PartOfSpeech] = {
    'd': PartOfSpeech.DETERMINER,
    'r': PartOfSpeech.ADVERB,
    'e': PartOfSpeech.INTERJECTION,
    'i': PartOfSpeech.ADPOSITION,
    'n': PartOfSpeech.NOUN,
    'u': None,
    'm': PartOfSpeech.CARDINAL,
    'p': PartOfSpeech.PRONOUN,
    'a': PartOfSpeech.DETERMINER,
    'c': PartOfSpeech.CONJUNCTION,
    'v': PartOfSpeech.VERB,
    't': None,
    'j': PartOfSpeech.ADJECTIVE
}
"""
Parts of Speech associated with the word frequency data sets that can be found at:
https://www.wordfrequency.info/intro.asp
"""
