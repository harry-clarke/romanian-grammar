import csv
from typing import Dict, List, Optional

from scripts.part_of_speech import PartOfSpeech, Row

PART_OF_SPEECH: Dict[str, PartOfSpeech] = {
    'conj': PartOfSpeech.CONJUNCTION,
    'prep': PartOfSpeech.ADPOSITION,
    'gen': None,
    'uncl': None,
    'num': PartOfSpeech.CARDINAL,
    'ord': None,
    'noc': PartOfSpeech.NOUN,
    'det': PartOfSpeech.DETERMINER,
    'lett': None,  # Letter
    'nop': PartOfSpeech.NOUN,
    'adv': PartOfSpeech.ADVERB,
    'verb': PartOfSpeech.VERB,
    'adj': PartOfSpeech.ADJECTIVE,
    'int': PartOfSpeech.INTERJECTION,
    'detp': PartOfSpeech.DETERMINER,
    'pron': PartOfSpeech.PRONOUN,
    'vmod': PartOfSpeech.AUXILIARY_VERB,
    'fore': None,  # Foreign
    'clo': None,
    'neg': None,  # Negation
    'ex': PartOfSpeech.INTERJECTION,
    'inf': None,  # Infinite marker ('to' do)

}


def _attach_headers(header: [str], row: [str]) -> Optional[Row]:
    if len(header) != len(row):
        print(f'Tossed out row: {row}')
        return None
    return dict(zip(header, row))


def _enrich_row(row: Row) -> None:
    row['PoS'] = PART_OF_SPEECH[row['PoS'].lower().strip('-')]
    row['lemma'] = row['Word']
    del row['']
    del row['Word']


def _collapse_rows(rows: List[Row]) -> List[Row]:
    new_rows = []
    cur_row: Dict[str, str] = rows.pop(0)
    for row in rows:
        if row is None or row['Word'] == '@':
            # This is a variant of cur_lemma or a tossed out row
            continue
        # This is its own word
        _enrich_row(cur_row)
        new_rows.append(cur_row)
        cur_row = row
    return new_rows


def read_file(file_path: str) -> List[Row]:
    with open(file_path, 'r', encoding='windows-1252') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        rows = [_attach_headers(header, row) for row in reader]
        rows = _collapse_rows(rows)
        rows = sorted(rows, key=lambda row: row['Freq'], reverse=True)
    return rows


def write_file(file_path: str, rows: List[Row]) -> None:
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(rows[0].keys())
        writer.writerows(list(row.values()) for row in rows)
