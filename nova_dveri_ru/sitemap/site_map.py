from pprint import pprint
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from lxml import etree

from nova_dveri_ru.data import BASE_URL


def get_links_to_sitemaps(robots_url) -> list:
    """
    Возвращает ссылки на все xml карты сайта
    :param robots_url: robots.txt link
    :return: список ссылок на карты сайта
    """
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.site_maps()


def get_links_from_sitemaps(site_maps):
    """
    Возвращает все ссылки со всех карт сайта
    :param site_maps: список ссылок на карты сайта
    :return: yield -> ссылка на страницу
    """
    for url in site_maps:
        response = requests.get(url)
        root = etree.fromstring(response.content)
        for element in root:
            yield element.getchildren()[0].text


if __name__ == '__main__':
    maps = get_links_to_sitemaps(urljoin(BASE_URL, 'robots.txt'))
    links = list(get_links_from_sitemaps(maps))
    pprint(links)
