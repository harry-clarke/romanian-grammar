#! python3
from pathlib import PurePath
from sys import argv
from time import sleep
from typing import Callable

from scripts.parsers.csvparser import CsvParser
from scripts.parsers.parser import Parser
from scripts.parsers.uk.ac.lancs.ucrel.bncfreq import BncFreqParser
from scripts.part_of_speech import Row
from scripts.translators.la.bab import BabTranslator
from scripts.translators.translator import Translator

PARSER = BncFreqParser()

TRANSLATOR: Translator = BabTranslator()


def add_translation(row: Row, to_language: str) -> int:
    pos = row['PoS']
    pos_translations = TRANSLATOR.get_translations('english', to_language, row['lemma'])
    if pos not in pos_translations:
        return 0
    translations = pos_translations[pos]
    for i, from_translation in enumerate(translations.keys()):
        row[f'lemmas_{to_language}_{i}_from'] = from_translation
        row[f'lemmas_{to_language}_{i}_to'] = ', '.join(translations[from_translation])
    return len(translations.keys())


def _rename_path(path: PurePath, f: Callable[[str], str]) -> str:
    return str(path.with_name(f(path.stem)))


def translate_file(file_path: str, parser: Parser, language: str, dry_run: bool):
    if dry_run:
        print('Dry run, no files being written')

    rows = parser.read_file(file_path)
    print(f'{len(rows)} rows')
    failed_rows = []
    max_columns = 0
    for c, row in enumerate(rows):
        try:
            columns = add_translation(row, language)
            if columns > max_columns:
                max_columns = columns
        except Exception as e:
            failed_rows.append(row)
            print(f'Row failure for row:\n{row}\n\n{e}')
        print(f'{100 * c / len(rows):.2f}%')
        sleep(0.2)

    header = rows[0]
    for c in range(max_columns):
        if f'lemmas_{language}_{c}_from' not in header:
            header[f'lemmas_{language}_{c}_from'] = ''
            header[f'lemmas_{language}_{c}_to'] = ''

    if dry_run:
        return

    cur_path = PurePath(file_path)
    if len(failed_rows) != 0:
        fail_path = _rename_path(cur_path, lambda cur_name: f'{cur_name}_{language}_errors.csv')
        parser.write_file(fail_path, failed_rows)

    write_path = _rename_path(cur_path, lambda cur_name: f'{cur_name}_{language}.csv')
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
