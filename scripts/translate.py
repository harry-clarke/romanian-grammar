#! python3
from time import sleep
from typing import Dict

from sys import argv
from pathlib import PurePath

from scripts.info.wordfrequency.part_of_speech import PART_OF_SPEECH, read_file, write_file
from scripts.la import bab


def add_translation(row: Dict[str, str], to_language: str) -> None:
    pos = PART_OF_SPEECH[row['PoS']]
    translations = bab.get_translations('english', to_language, row['lemma'])
    translation = '' if pos not in translations else translations[pos][0]
    row[f'lemma_{to_language}'] = translation


def translate_file(file_path: str, language: str):
    rows = read_file(file_path)
    failed_rows = []
    for i, row in enumerate(rows):
        try:
            add_translation(row, 'romanian')
        except Exception as e:
            failed_rows.append(row)
            print(f'Row failure for row:\n{row}\n\n{e}')
        print(f'{100 * i / len(rows):.2f}%')
        sleep(1.0)
    cur_path = PurePath(file_path)
    cur_name = cur_path.stem

    if len(failed_rows) != 0:
        fail_name = f'{cur_name}_{language}_errors.csv'
        fail_path = str(cur_path.with_name(fail_name))
        write_file(fail_path, failed_rows)

    write_name = f'{cur_name}_{language}.csv'
    write_path = str(cur_path.with_name(write_name))
    write_file(write_path, rows)


def main():
    if len(argv) == 1:
        raise ValueError('Please specify the csv to pull words from.\nWord frequency data sets that can be found at: '
                         'https://www.wordfrequency.info/intro.asp')
    if len(argv) == 2:
        raise ValueError('Please specify the language you wish to translate.')
    file_path = argv[1]
    language = argv[2].lower()
    translate_file(file_path, language)


if __name__ == '__main__':
    main()
