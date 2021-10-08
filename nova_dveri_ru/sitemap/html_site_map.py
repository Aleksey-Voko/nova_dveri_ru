from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from nova_dveri_ru.data import BASE_URL, HTML_SITE_MAP, USER_AGENT

HEADERS = {
    'User-Agent': USER_AGENT}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    print(url)
    print(response.status_code)
    print('=' * 30)
    return response.text


def get_sub_links_to_html_sitemap(html_code):
    links = [
        'ВХОДНЫЕ ДВЕРИ',
        'МЕЖКОМНАТНЫЕ ДВЕРИ',
        'ДВЕРНАЯ ФУРНИТУРА',
    ]
    soup = BeautifulSoup(html_code, 'html.parser')
    col_tag = soup.find('div', {'class': 'col-sm-6'})
    a_tags = col_tag.find_all('a')
    for a_tag in a_tags:
        if a_tag.text.strip() in links:
            yield a_tag.get('href').strip()


def get_page_links_to_html_sitemap(links):
    for link in links:
        response = requests.get(link, headers=HEADERS)
        print(link)
        print(response.status_code)
        print('=' * 30)
        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')
        pagination_tag = soup.find('ul', {'class': 'pagination'})
        li_tags = pagination_tag.find_all('li')
        last_href = li_tags[-1].find('a').get('href').strip()
        count = int(last_href.split('=')[-1])
        yield link
        for product_page in generate_page_links(link, count):
            yield product_page


def generate_page_links(link, count):
    for page in range(2, count + 1):
        yield f'{link}?page={page}'


def get_product_links(page_links):
    for link in page_links:
        response = requests.get(link, headers=HEADERS)
        print(link)
        print(response.status_code)
        print('=' * 30)
        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')
        product_tags = soup.find_all(
            'div', {'class': 'product-layout product-list col-xs-12'})
        for tag in product_tags:
            btn_tag = tag.find('a', {'class': 'btn'})
            yield btn_tag.get('href').strip()


if __name__ == '__main__':
    html_site_map = get_html(urljoin(BASE_URL, HTML_SITE_MAP))
    sub_links = get_sub_links_to_html_sitemap(html_site_map)
    p_links = get_page_links_to_html_sitemap(sub_links)
    product_links = list(get_product_links(p_links))
