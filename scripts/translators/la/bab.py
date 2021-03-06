from typing import List, Dict, Optional, Tuple

import requests
from lxml import html
from lxml.html import HtmlElement

from scripts.part_of_speech import PartOfSpeech
from scripts.translators.translator import Translator, Translations

SITE_URL = 'https://en.bab.la/'
__DICTIONARY_PATH = 'dictionary/'
__RESULTS_CONTAINER_XPATH = '//div[@class="content"][not(@id)]/div[@class="quick-results container"]'
__HEADER_XPATH = 'div/div[2][@class="qr-word"]/*/text()'
__HEADER_CLASS = 'quick-results-header'
__ENTRY_CLASS = 'quick-result-entry'
__TRANSLATION_XPATH = 'div//ul[@class="sense-group-results"]/li/a/text()'
__POS_XPATH = 'div[1]/span/text()'
__START_TERM_XPATH = 'div[1]/a[@class="babQuickResult"]/text()'

PART_OF_SPEECH: Dict[str, PartOfSpeech] = {
    'noun': PartOfSpeech.NOUN,
    'verb': PartOfSpeech.VERB,
    'pron': PartOfSpeech.PRONOUN,
    'prp': PartOfSpeech.ADPOSITION,
    'conj': PartOfSpeech.CONJUNCTION,
    'vb': PartOfSpeech.VERB,
    'adj': PartOfSpeech.ADJECTIVE,
    'interj': PartOfSpeech.INTERJECTION,
    'adv': PartOfSpeech.ADVERB,
    'abbreviation': None
}


def _request_translation(from_language: str, to_language: str, word: str) -> requests.Response:
    return requests.get(f'{SITE_URL}{__DICTIONARY_PATH}{from_language}-{to_language}/{word}')


def _parse_pos(pos: str) -> Optional[PartOfSpeech]:
    pos = pos.strip('{[]}.')
    if pos in PART_OF_SPEECH:
        return PART_OF_SPEECH[pos]
    else:
        raise TypeError(f'Unknown PoS for bab.la: "{pos}"')


def _parse_entry(entry: HtmlElement) -> Tuple[PartOfSpeech, str, List[str]]:
    """

    :param entry: A div.quick-result-option HTML element
    :return: A tuple of:
    * PoS for this element and a list
    * The word/term in English associated with this translation
    * A list of possible translations for the given word/term
    """
    pos = entry.xpath(__POS_XPATH)
    pos = None if len(pos) == 0 else _parse_pos(pos[0])

    start_term = entry.xpath(__START_TERM_XPATH)[0]

    words = entry.xpath(__TRANSLATION_XPATH)
    words = [word.replace('ţ', 'ț') for word in words]
    return pos, start_term, words


def _parse_translation_page(translation_page: bytes, language_to: str) -> Dict[PartOfSpeech, Dict[str, List[str]]]:
    tree: HtmlElement = html.fromstring(translation_page)
    containers: List[HtmlElement] = tree.xpath(__RESULTS_CONTAINER_XPATH)
    if len(containers) == 0:
        return {}
    assert len(containers) == 1
    container = containers[0]
    is_language = False
    entries = []
    for child in container.getchildren():
        if child.attrib['class'] == __HEADER_CLASS:
            language: str = child.xpath(__HEADER_XPATH)[0].lower()
            is_language = language_to in language
            continue
        if is_language and child.attrib['class'] == __ENTRY_CLASS \
                and len(child.xpath('div[@class="toc-links-header"]')) == 0 \
                and len(child.xpath('div[@class="quick-result-overview bab-full-width"]')) == 0:
            entries.append(child)

    translations = dict()
    for entry in entries:
        pos, start_term, entry_translations = _parse_entry(entry)
        if pos not in translations:
            translations[pos] = dict()
        pos_translations = translations[pos]
        if start_term not in pos_translations:
            pos_translations[start_term] = list()
        pos_translations[start_term] += entry_translations

    return translations


class BabTranslator(Translator):

    def get_translations(self, from_language: str, to_language: str, word: str) -> Translations:
        to_language = to_language.lower()
        try:
            translations = _parse_translation_page(
                _request_translation(from_language.lower(), to_language, word).content,
                to_language)
        except Exception as e:
            raise Exception(e,
                            {'from_language': from_language, 'to_language': to_language, 'word': word}).with_traceback(
                e.__traceback__)

        return translations


TEST_TRANSLATOR = BabTranslator()


def _test_1():
    ts = TEST_TRANSLATOR.get_translations('english', 'romanian', 'knife')
    assert ts == {PartOfSpeech.NOUN: {'knife': ['cuțit', 'tacâm']}}


def _test_2():
    ts = TEST_TRANSLATOR.get_translations('english', 'romanian', 'who')
    assert ts[PartOfSpeech.PRONOUN]['who'][0] == 'care'
    assert ts[PartOfSpeech.ADPOSITION]['who'] == ['de (care)']


def _test_3():
    ts = TEST_TRANSLATOR.get_translations('english', 'romanian', 'of')
    assert ts[PartOfSpeech.ADPOSITION] == {
        'of': ['a', 'dintre', 'despre', 'dintru (locul)', 'din (cu înțeles partitiv)', 'de (despre)',
               'de (arată originea)']}
    assert ts[PartOfSpeech.CONJUNCTION] == {'of': ['de']}


def _test_4():
    ts = TEST_TRANSLATOR.get_translations('english', 'romanian', 'every')
    assert ts == {PartOfSpeech.PRONOUN: {'every': ['fiecare', 'tot', 'toți', 'fiecare (implicând totalitatea)']},
                  None: {'every': ['fiecare']}}


def _test_5():
    ts = TEST_TRANSLATOR.get_translations('english', 'romanian', '1st')
    assert ts == {}


if __name__ == '__main__':
    _test_1()
    _test_2()
    _test_3()
    _test_4()
    _test_5()
