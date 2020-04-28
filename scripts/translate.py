#! python3
from typing import Dict, List

from sys import argv
import csv

from scripts.info.academicvocabulary.part_of_speech import PART_OF_SPEECH
from scripts.la import bab


def attach_headers(header: [str], row: [str]) -> Dict[str, str]:
    assert len(header) == len(row)
    return dict(zip(header, row))


def read_file(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        rows = [attach_headers(header, row) for row in reader]
    return rows


def write_file(file_path: str, rows: List[Dict[str, str]]) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(rows[0].keys())
        writer.writerows(row.values() for row in rows)


def add_translation(row: Dict[str, str], to_language: str) -> None:
    pos = PART_OF_SPEECH[row['PoS']]
    translations = bab.get_translations('english', to_language, row['lemma'])
    translation = '' if pos not in translations else translations[pos][0]
    row[f'lemma_{to_language}'] = translation


def main():
    file_path = argv[1]
    rows = read_file(file_path)[:10]
    for row in rows:
        add_translation(row, 'romanian')
    write_file(f'{file_path}.poof', rows)
    print(rows[0])


if __name__ == '__main__':
    main()
