from pathlib import Path
from urllib.parse import urljoin

from data import BASE_URL, HTML_SITE_MAP
from nova_dveri_ru.utils import add_in_yaml
from sitemap.html_site_map import (get_html,
                                   get_sub_links_to_html_sitemap,
                                   get_page_links_to_html_sitemap,
                                   get_product_links)


def main():
    product_links_file = 'output/product_links.yaml'

    if not Path(product_links_file).exists():
        html_site_map = get_html(urljoin(BASE_URL, HTML_SITE_MAP))
        sub_links = get_sub_links_to_html_sitemap(html_site_map)
        page_links = get_page_links_to_html_sitemap(sub_links)

        for link in get_product_links(page_links):
            print(link)
            add_in_yaml(link, product_links_file, flow_style=False)


if __name__ == '__main__':
    main()
