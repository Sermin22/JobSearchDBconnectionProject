from config import config
from src.db_manager import DBManager
from src.utils import create_database, create_table, save_data_to_database
from src.hh_api_empoyers import HeadHunterApiEmployers
from src.hh_api_vacancies import HeadHunterApiVacancies


def main():
    """Главная функция, которая подключается к PostgresSQL, создает базу base_vacancies, в базе данных
    создает таблицы employers и vacancies в base_vacancies. Далее используя реализованные классы
    и методы получает список вакансий, интересующих компаний работодателей по их ID и записывает
    данные в соответствующие таблицы в базе данных. С помощью класса DBManager и его методов из сформированной
    базы данных извлекает различные данные из таблиц"""

    # Получаем параметры для подключения к PostgresSQL
    params = config()
    # Записываем название базы данных
    database_name = 'base_vacancies'

    # Создаем базу base_vacancies
    create_database(database_name, params)

    # Создаем таблицы employers и vacancies в base_vacancies
    create_table(database_name, params)

    # Определяем список интересующих нас компаний работодателей
    interesting_employers = ['Tech Horizon', 'Кадровое агентство HireWay', 'Project Brain', 'Аптрейд',
                             'Кадровое агентство Candidate', 'ВижнЛабс VisionLabs', 'SberTech', 'Wildbox',
                             'LATOKEN', 'Enjoypro', 'RecruitTech', 'Таубина Софья Антоновна',
                             'Джем-Софт', 'kt.team']

    # Подключаясь к API hh.ru через класс HeadHunterApiEmployers получаем данные в виде списка,
    # содержащие ID компании работодателя, название, url и количество открытых вакансий
    list_interesting_employers = []
    for company in interesting_employers:
        hh_api_employers = HeadHunterApiEmployers()
        hh_employers = hh_api_employers.get_employers(company)
        list_interesting_employers.extend(hh_employers)

    # Подключаясь к API hh.ru через класс HeadHunterApiVacancies получаем список вакансий,
    # интересующих нас компаний работодателей по ID, полученных в list_interesting_companies
    interesting_employers_id = [key['id_employer'] for key in list_interesting_employers]

    # Создаем объект класса HeadHunterApiVacancies
    hh_api_vacancies = HeadHunterApiVacancies()

    # Получаем вакансии интересующих нас компаний по их ID
    hh_vacancies = hh_api_vacancies.get_vacancies('', interesting_employers_id)

    # Записываем полученные данные о работодателях и вакансиях в базу данных в соответствующие таблицы
    save_data_to_database(list_interesting_employers, hh_vacancies, database_name, params)

    # Создаем объект класса DBManager
    manager = DBManager(database_name, params)

    # Получаем список всех компаний и количество вакансий у каждой компании
    list_companies_and_vacancies_count = manager.get_companies_and_vacancies_count()
    print(list_companies_and_vacancies_count)

    # Получаем список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    list_all_vacancies = manager.get_all_vacancies()
    print(list_all_vacancies)

    # Получаем среднюю зарплату по вакансиям компаний
    avg_salary = manager.get_avg_salary()
    print(avg_salary)

    # Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям
    list_vacancies_with_higher_salary = manager.get_vacancies_with_higher_salary()
    print(list_vacancies_with_higher_salary)

    # Получаем список всех вакансий, в названии которых содержатся переданные в метод слова
    list_get_vacancies_with_keyword = manager.get_vacancies_with_keyword('разработчик')
    print(list_get_vacancies_with_keyword)


if __name__ == '__main__':
    main()
