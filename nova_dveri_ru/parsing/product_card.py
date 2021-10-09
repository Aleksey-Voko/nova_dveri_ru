from pprint import pprint

import requests
from bs4 import BeautifulSoup, element

from nova_dveri_ru.data import HEADERS


def get_meta_title(soup: BeautifulSoup):
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text
    else:
        return ''


def get_meta_description(soup: BeautifulSoup):
    meta_description_tag = soup.find(
        'meta', {'name': 'description'})
    if meta_description_tag:
        return meta_description_tag.get('content')
    else:
        return ''


def get_keywords(soup: BeautifulSoup):
    keywords_tag = soup.find('meta', {'name': 'keywords'})
    if keywords_tag:
        return keywords_tag.get('content')
    else:
        return ''


def get_breadcrumbs(soup: BeautifulSoup) -> list:
    breadcrumbs_list = []
    breadcrumb_tag = soup.find('ul', {'class': 'breadcrumb'})
    a_tags = breadcrumb_tag.find_all('a')
    for a_tag in a_tags[1:-1]:
        breadcrumbs_list.append(a_tag.text.strip())
    return breadcrumbs_list


def get_h1(soup: BeautifulSoup):
    h1_tag = soup.find('h1')
    return h1_tag.text.strip()


def get_price(soup: BeautifulSoup):
    price_tag = soup.find('div', {'class': 'new-price'})
    price_container_tag = price_tag.find(
        'span', {'class': 'product-price-container'})
    special_container_tag = price_tag.find(
        'span', {'class': 'product-special-container'})
    if price_container_tag:
        price_content = price_container_tag.text.strip()
    elif special_container_tag:
        price_content = special_container_tag.text.strip()
    else:
        price_content = price_tag.text.strip()
    price_content = price_content.replace('p.', '')
    price_content = price_content.replace(' ', '')

    return int(price_content)


def get_old_price(soup: BeautifulSoup):
    old_price_tag = soup.find('div', {'class': 'old-price'})
    if old_price_tag:
        old_price_container_tag = old_price_tag.find(
            'span', {'class': 'product-price-container'})
        old_special_container_tag = old_price_tag.find(
            'span', {'class': 'product-special-container'})
        if old_price_container_tag:
            price_content = old_price_container_tag.text.strip()
        elif old_special_container_tag:
            price_content = old_special_container_tag.text.strip()
        else:
            price_content = old_price_tag.text.strip()
        price_content = price_content.replace('p.', '')
        price_content = price_content.replace(' ', '')

        return int(price_content)
    else:
        return ''


def get_form_group_tags(soup: BeautifulSoup) -> list:
    div_product_tag = soup.find('div', {'id': 'product'})
    form_group_tags = div_product_tag.find_all(
        'div', {'class': 'form-group required'},
    )
    form_group_tags += div_product_tag.find_all(
        'div', {'class': 'form-group display-in-components'},
    )
    form_group_tags += div_product_tag.find_all(
        'div',
        {'class': 'form-group required display-in-components'},
    )
    return form_group_tags


def get_dim_metal_door(group_tag: element.Tag) -> list:
    radio_tags = group_tag.find_all('div', {'class': 'radio'})
    dimensions_metal_door = []
    for radio_tag in radio_tags:
        label_tag = radio_tag.find('label')
        dimensions_metal_door.append(list(label_tag.children)[-1].strip())
    return dimensions_metal_door


def get_opening_type(group_tag: element.Tag) -> list:
    img_tags = group_tag.find_all('img')
    opening_type = []
    for img_tag in img_tags:
        opening_type.append({
            'title': img_tag.get('title'),
            'src': img_tag.get('src'),
        })
    return opening_type


def get_choose_a_color(group_tag: element.Tag) -> list:
    radio_tags = group_tag.find_all('div', {'class': 'radio input-image'})
    choose_a_color = []
    for radio_tag in radio_tags:
        input_tag = radio_tag.find('input', {'type': 'radio'})
        img_tag = radio_tag.find('img')
        choose_a_color.append({
            'title': img_tag.get('title'),
            'src': img_tag.get('src'),
            'value_id': input_tag.get('value'),
        })
    return choose_a_color


def get_door_size(group_tag: element.Tag) -> list:
    select_tag = group_tag.find('select', {'data-option-id': '18'})
    option_tags = select_tag.find_all('option', {'data-option-id': '18'})
    door_size = []
    for option_tag in option_tags:
        door_size.append({
            'value': option_tag.get('data-option-value-name'),
            'price_plus': option_tag.get('data-option-value-price')
        })
    return door_size


def get_door_frame(group_tag: element.Tag) -> list:
    select_tag = group_tag.find('select', {'data-option-id': '15'})
    option_tags = select_tag.find_all('option', {'data-option-id': '15'})
    door_frame = []
    for option_tag in option_tags:
        door_frame.append({
            'value': option_tag.get('data-option-value-name'),
            'price': option_tag.get('data-option-value-price')
        })
    return door_frame


def get_platband(group_tag: element.Tag) -> list:
    select_tag = group_tag.find('select', {'data-option-id': '16'})
    option_tags = select_tag.find_all('option', {'data-option-id': '16'})
    platband = []
    for option_tag in option_tags:
        platband.append({
            'value': option_tag.get('data-option-value-name'),
            'price': option_tag.get('data-option-value-price')
        })
    return platband


def get_board(group_tag: element.Tag) -> list:
    select_tag = group_tag.find('select', {'data-option-id': '17'})
    option_tags = select_tag.find_all('option', {'data-option-id': '17'})
    board = []
    for option_tag in option_tags:
        board.append({
            'value': option_tag.get('data-option-value-name'),
            'price': option_tag.get('data-option-value-price')
        })
    return board


def get_description(soup: BeautifulSoup) -> list:
    description_tag = soup.find('div', {'id': 'tab-description'})
    desc_contents = [
        x for x in description_tag.contents
        if x and x != '\n'
    ]
    description = []
    if description_tag and desc_contents:

        table_100_tag = description_tag.find('table', {'width': '100%'})
        if table_100_tag:
            group = {'Описание': {}}
            tr_tags = table_100_tag.find_all('tr')
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all('td')
                key = td_tags[0].text.strip()
                value = td_tags[-1].text.strip()
                group['Описание'][key] = value
            description.append(group)

        else:
            if not description_tag.find('div'):
                first_p_tag = description_tag.find('p')
                if first_p_tag:
                    strong_p_tag = first_p_tag.find('strong')
                    if not strong_p_tag:
                        description.append(first_p_tag.text.strip())

                strong_tags = description_tag.find_all('strong')
                for strong_tag in strong_tags:
                    name_group = strong_tag.text.strip()
                    group = {name_group: {}}
                    table_tag = strong_tag.parent.next_sibling.next_sibling
                    tr_tags = table_tag.find_all('tr')
                    for tr_tag in tr_tags:
                        td_tags = tr_tag.find_all('td')
                        if len(td_tags) == 3:
                            p_key = td_tags[0].find('p')
                            if p_key:
                                key = p_key.text.strip()
                            else:
                                key = td_tags[0].text.strip()
                            p_value = td_tags[-1].find('p')
                            if p_value:
                                value = p_value.text.strip()
                            else:
                                value = td_tags[-1].text.strip()
                            group[name_group][key] = value
                    description.append(group)

            if not description:
                description.append(str(description_tag))

    return description


def get_specification(soup: BeautifulSoup) -> list:
    specification_tag = soup.find('div', {'id': 'tab-specification'})
    specification = []
    if specification_tag:
        group = {}
        name_group = ''

        div_row_tags = specification_tag.find_all(
            'div', {'class': 'row'})
        for div_row_tag in div_row_tags:
            key, value = '', ''
            div_col_sm_12_tag = div_row_tag.find(
                'div', {'class': 'col-sm-12'})
            if div_col_sm_12_tag:
                if group:
                    specification.append(group)
                div_head_td_tag = div_col_sm_12_tag.find(
                    'div', {'class': 'head-td'})
                strong_tag = div_head_td_tag.find('strong')
                name_group = strong_tag.text.strip()
                group = {name_group: {}}
            div_col_sm_5_tag = div_row_tag.find(
                'div', {'class': 'col-sm-5 col-xs-6'})
            if div_col_sm_5_tag:
                attr_td_tag = div_col_sm_5_tag.find(
                    'div', {'class': 'attr-td'})
                key = attr_td_tag.text.strip()
            div_col_sm_7_tag = div_row_tag.find(
                'div', {'class': 'col-sm-7 col-xs-6'})
            if div_col_sm_7_tag:
                attr_td_tag = div_col_sm_7_tag.find(
                    'div', {'class': 'attr-td'})
                value = attr_td_tag.text.strip()
            if key and value:
                group[name_group][key] = value

        if group:
            specification.append(group)

    return specification


def get_images(soup: BeautifulSoup) -> list:
    images = []
    slider_tag = soup.find('div', {'class': 'slider-bigthumb'})
    if slider_tag:
        div_tags = slider_tag.find_all('div')
        for div_tag in div_tags:
            value_id = div_tag.get('data-option')
            a_tag = div_tag.find('a')
            link = a_tag.get('href')
            images.append({
                'value_id': value_id,
                'link': link,
            })
    else:
        slider_tag = soup.find('div', {'class': 'none-slider-bigthumb'})
        a_tag = slider_tag.find('a')
        link = a_tag.get('href')
        images.append({'link': link,})

    return images


def get_product_card(link, sess: requests.sessions.Session) -> dict:
    product_card = {}

    while True:
        try:

            response = sess.get(link, headers=HEADERS)
            if response.status_code == requests.codes.ok:
                print(response.url, 'request ok', sep=' -> ')
                print('status_code', str(response.status_code), sep=' -> ')

                html_code = response.text
                soup = BeautifulSoup(html_code, 'html.parser')

                product_card['link'] = link
                product_card['meta_title'] = get_meta_title(soup)
                product_card['meta_description'] = get_meta_description(soup)
                product_card['keywords'] = get_keywords(soup)
                product_card['breadcrumbs'] = get_breadcrumbs(soup)
                product_card['h1'] = get_h1(soup)
                product_card['price'] = get_price(soup)
                product_card['old_price'] = get_old_price(soup)

                # brand
                # code
                # availability
                product_info = soup.find('div', {'class': 'product-info'})
                list_unstyled_tag = product_info.find(
                    'ul', {'class': 'list-unstyled'})
                li_tags = list_unstyled_tag.find_all('li')
                for li_tag in li_tags:
                    span_tag = li_tag.find('span')
                    text_tag = span_tag.text.strip()
                    if text_tag == 'Производитель:':
                        a_tag = li_tag.find('a')
                        product_card['brand'] = a_tag.text.strip()
                    elif text_tag == 'Код товара:':
                        product_card['code'] = li_tag.contents[1].text.strip()
                    elif text_tag == 'Доступность:':
                        stock_status_tag = li_tag.find(
                            'span', {'class': 'stock_status'})
                        stock_status = stock_status_tag.get('data-stock')
                        product_card['availability'] = stock_status.strip()

                # Доступные опции
                form_group_tags = get_form_group_tags(soup)
                for group_tag in form_group_tags:
                    control_label_tag = group_tag.find(
                        'label', {'class': 'control-label option-label'})
                    text_tag = control_label_tag.text.strip()

                    if text_tag == 'Размер двери металлической':
                        product_card[text_tag] = get_dim_metal_door(group_tag)
                    elif text_tag == 'Тип открывания':
                        product_card[text_tag] = get_opening_type(group_tag)
                    elif text_tag == 'Выберите цвет':
                        product_card[text_tag] = get_choose_a_color(group_tag)
                    elif text_tag == 'Выберите размер двери':
                        product_card[text_tag] = get_door_size(group_tag)
                    elif text_tag == 'Коробка':
                        product_card[text_tag] = get_door_frame(group_tag)
                    elif text_tag == 'Наличник':
                        product_card[text_tag] = get_platband(group_tag)
                    elif text_tag == 'Добор':
                        product_card[text_tag] = get_board(group_tag)

                product_card['Описание'] = get_description(soup)
                product_card['Характеристики'] = get_specification(soup)
                product_card['images'] = get_images(soup)

                break
                ####################

            elif response.status_code == 404:
                product_card = {}
                print(response.url + '\n',
                      '!!! Get link request failed !!!'.upper(), sep=' -> ')
                print('status_code', str(response.status_code), sep=' -> ')
                break
            else:
                print(response.url + '\n',
                      '!!! Get link request failed !!!'.upper(), sep=' -> ')
                print('status_code', str(response.status_code), sep=' -> ')

            print('=' * 100)
            print()
            continue

        except Exception as e:
            print(('#' * 20) + '  Exception  ' + ('#' * 20))
            print(link)
            print(e)
            print(('#' * 20) + '  Exception  ' + ('#' * 20))
            print()
            # continue

    return product_card


def get_product_cards(links):
    with requests.Session() as sess:
        for link in links:
            product_card = get_product_card(link, sess)
            if product_card.keys():
                yield product_card


if __name__ == '__main__':
    lnk = 'https://nova-dveri.ru/vhodnye-dveri/proizvodstvo-rossiya/sudar/-vhodnaja-dver-md-510-latte'
    with requests.Session() as s:
        p_card = get_product_card(lnk, s)
        pprint(p_card)
