import argparse
import csv
import statistics
from collections import defaultdict
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description='Generate report on median coffee spending per student.')
    parser.add_argument('--files', nargs='+', required=True, help='List of CSV files to process')
    parser.add_argument('--report', required=True, help='Name of the report (e.g., median-coffee)')
    return parser.parse_args()

def read_coffee_data(file_paths):
    coffee_spent = defaultdict(list)
    for file_path in file_paths:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                student = row.get('student')
                try:
                    amount = float(row.get('coffee_spent', 0))
                except (ValueError, TypeError):
                    continue
                if student:
                    coffee_spent[student].append(amount)
    return coffee_spent

def calculate_medians(coffee_spent):
    medians = []
    for student, amounts in coffee_spent.items():
        if amounts:
            median_value = statistics.median(amounts)
            medians.append((student, median_value))
    return medians

def generate_report(medians, report_name):
    # Сортировка по убыванию медианы
    medians_sorted = sorted(medians, key=lambda x: x[1], reverse=True)
    headers = ['Student', f'{report_name}']
    print(tabulate(medians_sorted, headers=headers, floatfmt=".2f"))

def main():
    args = parse_args()
    coffee_data = read_coffee_data(args.files)
    medians = calculate_medians(coffee_data)
    generate_report(medians, args.report) 
     
main()
