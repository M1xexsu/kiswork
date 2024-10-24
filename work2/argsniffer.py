import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="PlantUML visualizer")
    parser.add_argument('-p', '--package', required=False, help='Имя анализируемого пакета')
    parser.add_argument('-f', '--filesystem', required=True, help='Путь к файлу с изображением графа зависимостей')
    parser.add_argument('-d', '--depth', required=True, help='Максимальная глубина анализа зависимостей')
    return parser.parse_args()
