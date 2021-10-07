from nova_dveri_ru.data import BASE_URL
from nova_dveri_ru.sitemap.site_map import get_robots


def main():
    robot = get_robots(f'{BASE_URL}robots.txt')
    print(robot)


if __name__ == '__main__':
    main()
