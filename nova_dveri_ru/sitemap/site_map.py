from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

from nova_dveri_ru.data import BASE_URL


def get_site_maps(url) -> list:
    rp = RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp.site_maps()


if __name__ == '__main__':
    site_maps = get_site_maps(urljoin(BASE_URL, 'robots.txt'))
    print(site_maps)
