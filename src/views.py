from config import config
from src.utils import create_database, create_table, save_data_to_database
from src.hh_api_empoyers import HeadHunterApiEmployers
from src.hh_api_vacancies import HeadHunterApiVacancies


def main():
    """Главная функция..."""

    # Получаем параметры для подключения к PostgresSQL
    params = config()

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
    hh_api_vacancies = HeadHunterApiVacancies()
    hh_vacancies = hh_api_vacancies.get_vacancies('', interesting_employers_id)

    save_data_to_database(list_interesting_employers, hh_vacancies, database_name, params)


if __name__ == '__main__':
    main()