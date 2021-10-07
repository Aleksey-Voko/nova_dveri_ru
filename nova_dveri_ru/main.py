from pprint import pprint
from urllib.parse import urljoin

from nova_dveri_ru.data import BASE_URL
from nova_dveri_ru.sitemap.site_map import get_links_to_sitemaps,\
    get_links_from_sitemaps


def main():
    maps = get_links_to_sitemaps(urljoin(BASE_URL, 'robots.txt'))
    links = list(get_links_from_sitemaps(maps))
    pprint(links)


if __name__ == '__main__':
    main()
