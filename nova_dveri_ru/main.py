from urllib.parse import urljoin

from nova_dveri_ru.data import BASE_URL
from nova_dveri_ru.sitemap.site_map import get_site_maps


def main():
    site_maps = get_site_maps(urljoin(BASE_URL, 'robots.txt'))
    print(site_maps)


if __name__ == '__main__':
    main()
