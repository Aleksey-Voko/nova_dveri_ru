from urllib.parse import urljoin

from data import BASE_URL, HTML_SITE_MAP
from sitemap.html_site_map import (get_html,
                                   get_sub_links_to_html_sitemap,
                                   get_page_links_to_html_sitemap,
                                   get_product_links)


def main():
    html_site_map = get_html(urljoin(BASE_URL, HTML_SITE_MAP))
    sub_links = get_sub_links_to_html_sitemap(html_site_map)
    page_links = get_page_links_to_html_sitemap(sub_links)
    product_links = list(get_product_links(page_links))


if __name__ == '__main__':
    main()
