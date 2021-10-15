import json

from nova_dveri_ru.utils import get_from_yaml


card_list = list(get_from_yaml('output/product_cards.yaml'))
indent = ' ' * 4
with open('output/product_cards.json', 'w', encoding='utf-8') as json_out:
    json.dump(card_list, json_out, ensure_ascii=False, indent=indent)
