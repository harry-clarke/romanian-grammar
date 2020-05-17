from typing import List

from scripts.part_of_speech import Row


class Parser:
    def write_file(self, file_path: str, rows: List[Row]) -> None: ...
    def read_file(self, file_path: str) -> List[Row]: ...
