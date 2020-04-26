import requests
from lxml import html

SITE_URL = 'https://en.bab.la/'
__DICTIONARY_PATH = 'dictionary/'
__TRANSLATION_XPATH = '//div[@class="content"][not(@id)]/div/div[2]/div[2]/ul[@class="sense-group-results"]/li/a/text()'


def _request_translation(from_language: str, to_language: str, word: str) -> requests.Response:
    return requests.get(f'{SITE_URL}{__DICTIONARY_PATH}{from_language}-{to_language}/{word}')


def _parse_translation_page(translation_page: bytes) -> [str]:
    tree = html.fromstring(translation_page)
    words = tree.xpath(__TRANSLATION_XPATH)
    return [word.replace('ţ', 'ț') for word in words]


def get_translations(from_language: str, to_language: str, word: str) -> [str]:
    return _parse_translation_page(_request_translation(from_language.lower(), to_language.lower(), word).content)


def _test_1():
    ts = get_translations('english', 'romanian', 'knife')
    assert ts == ['cuțit', 'tacâm']


if __name__ == '__main__':
    _test_1()
