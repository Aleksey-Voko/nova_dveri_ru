import requests

from nova_dveri_ru.data import USER_AGENT


def save_html_code(input_url: str, out_file: str):
    headers = {
        'User-Agent': USER_AGENT,
    }
    response = requests.get(input_url, headers=headers)
    html_code = response.text

    with open(out_file, 'w', encoding='utf-8') as fl:
        fl.write(html_code)


if __name__ == '__main__':
    url = 'https://nova-dveri.ru/dvernaya-furnitura/'
    out_html_file = 'dvernaya-furnitura.html'
    save_html_code(url, out_html_file)
