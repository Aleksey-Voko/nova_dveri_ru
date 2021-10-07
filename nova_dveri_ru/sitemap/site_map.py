import requests

from nova_dveri_ru.data import BASE_URL


def get_robots(url):
    return requests.get(url).text


if __name__ == '__main__':
    robot = get_robots(f'{BASE_URL}robots.txt')
    print(robot)
