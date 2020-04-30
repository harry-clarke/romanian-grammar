from enum import Enum, auto
from typing import Dict, Union


class PartOfSpeech(Enum):
    ADJECTIVE = auto()
    ADVERB = auto()
    NOUN = auto()
    VERB = auto()
    INTERJECTION = auto()
    AUXILIARY_VERB = auto()
    CLITIC = auto()
    COVERB = auto()
    CONJUNCTION = auto()
    DETERMINER = auto()
    PARTICLE = auto()
    CLASSIFIER = auto()
    ADPOSITION = auto()
    PREVERB = auto()
    PRONOUN = auto()
    CONTRACTION = auto()
    CARDINAL = auto()


Row = Dict[str, Union[str, PartOfSpeech]]