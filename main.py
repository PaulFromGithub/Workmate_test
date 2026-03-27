import argparse
import csv
import statistics
from collections import defaultdict
from tabulate import tabulate



def median_coffee_report(data):
    """Генерирует отчет по медиане трат на кофе"""
    results = []
    for student, amounts in data.items():
        if amounts:
            median_value = statistics.median(amounts)
            results.append((student, median_value))
    return sorted(results, key=lambda x: x[1], reverse=True)

# Добавляем второй пример отчета
def total_spent_report(data):
    """Генерирует отчет по общей сумме трат"""
    results = []
    for student, amounts in data.items():
        if amounts:
            total = sum(amounts)
            results.append((student, total))
    return sorted(results, key=lambda x: x[1], reverse=True)

reports = {'median-coffee': median_coffee_report,
           'total-spent': total_spent_report 
} 

def parse_args():
    """ Получение входных данных """
    parser = argparse.ArgumentParser(description='Генерация отчетов по данным студентов')
    parser.add_argument('--files', nargs='+', required=True, help='Список файлов')
    parser.add_argument('--report', required=True, help='Название отчета')
    file_paths = parser.parse_args()
    return file_paths

def read_data(file_paths):
    """ Цикл по файлам """
    data_dict = defaultdict(list)
    for file_path in file_paths:
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f) # Читаем файл как словарь
                for row in reader: 
                    student = row.get('student')
                    try:
                        amount = float(row.get('coffee_spent', 0)) 
                    except (ValueError, TypeError):
                        continue
                    if student:
                        data_dict[student].append(amount)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
    return data_dict

def generate_report(data, report_name):
    """ Создание таблицы """
    if report_name not in reports: # Проверяем, существует ли запрошенный отчет в нашем словаре
        print(f"Ошибка: Отчет '{report_name}' не найден.")
        print(f"Доступные отчеты: {', '.join(reports.keys())}")
        return # Останавливаем выполнение, если отчет неизвестен
    
    report_function = reports[report_name] # Вызываем нужную функцию из словаря и получаем результат
    results = report_function(data) 
    
    pretty_name = report_name.replace('-', ' ').title() # Формируем заголовок
    headers = ['Студент', pretty_name]
    
    print(tabulate( # Вывод таблицы
        results,
        headers=headers,
        floatfmt=".2f",
        tablefmt='grid'
    ))


def main():
    try:
        parse_args()
    except SystemExit:
        return 
    
    data_dict = read_data(parse_args().files) # Читаем данные 
    generate_report(data_dict, parse_args().report) # Передаем данные и имя отчета
     
main()