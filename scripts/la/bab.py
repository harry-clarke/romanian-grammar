from typing import List, Dict, Optional

import bidict as bidict
import requests
from lxml import html
from lxml.html import HtmlElement

from scripts.part_of_speech import PartOfSpeech

SITE_URL = 'https://en.bab.la/'
__DICTIONARY_PATH = 'dictionary/'
__ENTRY_XPATH = '//div[@class="content"][not(@id)]/div[@class="quick-results container"]' \
                '/div[@class="quick-result-entry"]'
__TRANSLATION_XPATH = 'div//ul[@class="sense-group-results"]/li/a/text()'
__POS_XPATH = 'div[1]/span/text()'

PART_OF_SPEECH: Dict[str, PartOfSpeech] = {
    'noun': PartOfSpeech.NOUN,
    'verb': PartOfSpeech.VERB,
    'pron': PartOfSpeech.PRONOUN,
    'prp': PartOfSpeech.ADPOSITION,
    'conj': PartOfSpeech.CONJUNCTION
}


def _request_translation(from_language: str, to_language: str, word: str) -> requests.Response:
    return requests.get(f'{SITE_URL}{__DICTIONARY_PATH}{from_language}-{to_language}/{word}')


def _parse_pos(pos: str) -> Optional[PartOfSpeech]:
    pos = pos.strip('{}.')
    if pos in PART_OF_SPEECH:
        return PART_OF_SPEECH[pos]
    else:
        raise TypeError(f'Unknown PoS for bab.la: "{pos}"')


def _parse_translation_page(translation_page: bytes) -> Dict[PartOfSpeech, List[str]]:
    tree: HtmlElement = html.fromstring(translation_page)
    entries: List[HtmlElement] = tree.xpath(__ENTRY_XPATH)
    entries = list(filter(lambda e: len(e.xpath('div[@class="toc-links-header"]')) == 0, entries))
    translations = dict()
    for entry in entries:
        pos = entry.xpath(__POS_XPATH)[0]
        pos = _parse_pos(pos)
        words = entry.xpath(__TRANSLATION_XPATH)
        words = [word.replace('ţ', 'ț') for word in words]
        translations[pos] = words
    return translations


def get_translations(from_language: str, to_language: str, word: str) -> Dict[PartOfSpeech, List[str]]:
    return _parse_translation_page(_request_translation(from_language.lower(), to_language.lower(), word).content)


def get_translations_batch(from_language: str, to_language: str, words: List[str]) -> List[List[str]]:
    pass


def _test_1():
    ts = get_translations('english', 'romanian', 'knife')
    assert ts == {PartOfSpeech.NOUN: ['cuțit', 'tacâm']}


def _test_2():
    ts = get_translations('english', 'romanian', 'who')
    print(ts)


if __name__ == '__main__':
    _test_1()
    _test_2()
