import pytest
from collections import defaultdict
import main


TEST_DATA_PATH = "./test_data/test_data.csv"

@pytest.fixture
def sample_data():
    return main.read_data([TEST_DATA_PATH])

def test_read_data(sample_data):
    assert isinstance(sample_data, defaultdict), "Данные должны быть в defaultdict"
    
    assert "Ivan" in sample_data, "Студент Ivan должен быть в данных" # Проверяем наличие студентов
    assert "Olga" in sample_data, "Студент Olga должен быть в данных"
    
    assert sample_data["Ivan"] == [100.0, 200.0], "Траты Ivan должны быть [100.0, 200.0]" # Проверяем конкретные значения трат
    assert sample_data["Olga"] == [50.0, 150.0, 250.0], "Траты Olga должны быть [50.0, 150.0, 250.0]"
    
def test_median_coffee_report(sample_data):

    result = main.median_coffee_report(sample_data)
    result_dict = dict(result)
    
    assert result_dict["Ivan"] == 150.0, "Медиана Ivan должна быть 150"
    assert result_dict["Olga"] == 150.0, "Медиана Olga должна быть 150"
    
    assert result[0][0] == "Petr", "Первым должен быть Petr, медиана 300" # Проверяем сортировку по убыванию медианы
    assert result[0][1] == 300.0
    
    

def test_total_spent_report(sample_data):
    
    result = main.total_spent_report(sample_data)
    
    assert result[0][0] == "Olga", "Первым должна быть Olga сумма 450"
    assert result[0][1] == 450.0

def test_report_factory():
    
    assert 'median-coffee' in main.reports, "Отчет median-coffee должен быть зарегистрирован" # Проверяем наличие ключей в словаре reports
    assert 'total-spent' in main.reports, "Отчет total-spent должен быть зарегистрирован"
    
