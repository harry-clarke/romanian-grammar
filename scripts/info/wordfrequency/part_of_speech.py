import csv
from typing import Dict, List

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


def _attach_headers(header: [str], row: [str]) -> Dict[str, str]:
    assert len(header) == len(row)
    return dict(zip(header, row))


def read_file(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        rows = [_attach_headers(header, row) for row in reader]
    return rows


def write_file(file_path: str, rows: List[Dict[str, str]]) -> None:
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(rows[0].keys())
        writer.writerows(list(row.values()) for row in rows)