#! python3
from time import sleep

from sys import argv
from pathlib import PurePath
from typing import Callable

from scripts.parsers.csvparser import CsvParser
from scripts.parsers.info.wordfrequency.wordfrequency import WordFrequencyParser
from scripts.parsers.uk.ac.lancs.ucrel.bncfreq import BncFreqParser
from scripts.part_of_speech import Row
from scripts.translators.la import bab
from scripts.parsers.parser import Parser

PARSER = CsvParser()


def add_translation(row: Row, to_language: str) -> None:
    pos = row['PoS']
    translations = bab.get_translations('english', to_language, row['lemma'])
    translation = '' if pos not in translations else translations[pos][0]
    row[f'lemma_{to_language}'] = translation


def _rename_path(path: PurePath, f: Callable[[str], str]) -> str:
    return str(path.with_name(f(path.name)))


def translate_file(file_path: str, parser: Parser, language: str, dry_run: bool):
    if dry_run:
        print('Dry run, no files being written')

    rows = parser.read_file(file_path)
    print(f'{len(rows)} rows')
    failed_rows = []
    for i, row in enumerate(rows):
        try:
            add_translation(row, 'romanian')
        except Exception as e:
            failed_rows.append(row)
            print(f'Row failure for row:\n{row}\n\n{e}')
        print(f'{100 * i / len(rows):.2f}%')
        sleep(1.0)

    if dry_run:
        return

    cur_path = PurePath(file_path)
    if len(failed_rows) != 0:
        fail_path = _rename_path(cur_path, lambda cur_name: f'{cur_name}_{language}_errors.csv')
        parser.write_file(fail_path, failed_rows)

    write_path = _rename_path(lambda cur_name: f'{cur_name}_{language}.csv')
    parser.write_file(write_path, rows)


def main():
    if len(argv) == 1:
        raise ValueError('Please specify the csv to pull words from.\nWord frequency data sets that can be found at: '
                         'https://www.wordfrequency.info/intro.asp')
    if len(argv) == 2:
        raise ValueError('Please specify the language you wish to translate.')
    file_path = argv[1]
    language = argv[2].lower()
    dry_run = len(argv) >= 4 and argv[3] == '--dry-run'
    translate_file(file_path, PARSER, language, dry_run)


if __name__ == '__main__':
    main()
