from pathlib import Path
from urllib.parse import urljoin

from data import BASE_URL, HTML_SITE_MAP
from parsing.product_card import get_product_cards
from utils import add_in_yaml, get_from_yaml
from sitemap.html_site_map import (get_html,
                                   get_sub_links_to_html_sitemap,
                                   get_page_links_to_html_sitemap,
                                   get_product_links)


def main():
    product_links_file = 'output/product_links.yaml'
    product_cards_file = 'output/product_cards.yaml'

    if not Path(product_links_file).exists():
        html_site_map = get_html(urljoin(BASE_URL, HTML_SITE_MAP))
        sub_links = get_sub_links_to_html_sitemap(html_site_map)
        page_links = get_page_links_to_html_sitemap(sub_links)

        for link in get_product_links(page_links):
            print(link)
            add_in_yaml(link, product_links_file, flow_style=False)

    product_links = get_from_yaml(product_links_file)
    if Path(product_cards_file).exists():
        product_cards = get_from_yaml(product_cards_file)
        completed_links = [x['link'] for x in product_cards]
    else:
        completed_links = []

    product_links = list(set(product_links) - set(completed_links))
    for product_card in get_product_cards(product_links):
        add_in_yaml(product_card, product_cards_file, flow_style=False)
        completed_links.append(product_card['link'])
        print('=' * 100)
        print()


if __name__ == '__main__':
    main()
