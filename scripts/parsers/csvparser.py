import csv
from pickle import load, loads
from typing import List

from scripts.parsers.parser import Parser
from scripts.part_of_speech import Row, PartOfSpeech


class CsvParser(Parser):

    @staticmethod
    def _attach_headers(header: [str], row: [str]) -> Row:
        assert len(header) == len(row)
        return dict(zip(header, row))

    def enrich_row(self, row):
        if row['PoS'] == '':
            pos = None
        else:
            pos = eval(row['PoS'])
        assert pos is None or isinstance(pos, PartOfSpeech)
        row['PoS'] = pos

    def read_file(self, file_path: str) -> List[Row]:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            rows = [CsvParser._attach_headers(header, row) for row in reader]
            for row in rows:
                self.enrich_row(row)
            return rows
            # return map(lambda r: _attach_headers(header, r), reader)

    def write_file(self, file_path: str, rows: List[Row]) -> None:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(rows[0].keys())
            writer.writerows(list(row.values()) for row in rows)
