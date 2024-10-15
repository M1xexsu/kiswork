import argparse

def parse_args():
    user = "defaultuser"
    host = "localhost"
    parser = argparse.ArgumentParser(description="Эмулятор как можно более похожий на сеанс в UNIX-подобной ОС")
    parser.add_argument('-u', '--user', required=False, help='Имя пользователя')
    parser.add_argument('-v', '--host', required=False, help='Имя машины')
    parser.add_argument('-f', '--filesystem', required=True, help='Путь к архиву "файловой системы"')
    parser.add_argument('-l', '--logfile', required=True, help='Путь к логам')
    parser.add_argument('-s', '--script', required=False, help='Стартовый скрипт')
    return parser.parse_args()
