import psycopg2
from config import config


class DBManager:
    database_name: str
    params: dict

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.conn = None
        self.params = params

    def connect(self):
        try:
            # Подключаемся к базе данных с параметрами из файла и именем базы данных
            self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
            print(f"Подключено к базе данных PostgreSQL: {self.database_name}")
        except Exception as error:
            print(f"Ошибка при подключении к PostgreSQL: {error}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(f"Отключено от базы данных PostgreSQL: {self.database_name}")

    def get_companies_and_vacancies_count(self):
        '''Метод получает список всех компаний и количество вакансий у каждой компании'''

        self.connect()  # Устанавливаем соединение
        if not self.conn:
            raise RuntimeError("Соединение не установлено.")

        cur = self.conn.cursor()
        query = """
            SELECT
                employers.id_employer,
                employers.name_employer,
                COUNT(vacancies.id_vacancy) AS number_of_vacancies
            FROM
                employers
            LEFT JOIN vacancies
            ON
                employers.id_employer = vacancies.id_employer
            GROUP BY
            employers.id_employer;
                """
        try:
            cur.execute(query)
            result = cur.fetchall()
            # return result
            result_list = []
            for id_employer, name_employer, number_of_vacancies in result:
                result_list.append(f"id_employer: {id_employer}, name_employer: {name_employer}, "
                                   f"number_of_vacancies: {number_of_vacancies}")
            return result_list

        except Exception as error:
            print(f"Ошибка выполнения запроса: {error}")
            return []
        finally:
            cur.close()
            self.disconnect()  # Разрываем соединение

    def get_all_vacancies(self):
        '''Метод получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию'''

        self.connect()  # Устанавливаем соединение
        if not self.conn:
            raise RuntimeError("Соединение не установлено.")

        cur = self.conn.cursor()
        query = """
            SELECT
                employers.name_employer,
                name_vacancy,
                salary_from,
                salary_to,
                vacancies_url
            FROM
                employers
            JOIN
                vacancies
            ON
                employers.id_employer = vacancies.id_employer;
                """
        try:
            cur.execute(query)
            result = cur.fetchall()
            # return result
            vacancies_list = []
            for name_employer, name_vacancy, salary_from, salary_to, vacancies_url in result:
                vacancies_list.append(f"name_employer: {name_employer}, name_vacancy: {name_vacancy}, "
                                      f"Salary: от {salary_from} до {salary_to}, vacancies_url: {vacancies_url}")
            return vacancies_list

        except Exception as error:
            print(f"Ошибка выполнения запроса: {error}")
            return []
        finally:
            cur.close()
            self.disconnect()  # Разрываем соединение

    def get_avg_salary(self):
        '''Метод получает среднюю зарплату по вакансиям компаний'''

        self.connect()  # Устанавливаем соединение
        if not self.conn:
            raise RuntimeError("Соединение не установлено.")

        cur = self.conn.cursor()
        query = """
            SELECT
                name_employer,
                AVG(salary_from) AS average_salary_from
            FROM
                vacancies
            GROUP BY
                name_employer;
                """
        try:
            cur.execute(query)
            result = cur.fetchall()
            # return result
            result_list = []
            for name_employer, average_salary_from in result:
                result_list.append(f"name_employer: {name_employer}, average_salary_from: {average_salary_from}")
            return result_list

        except Exception as error:
            print(f"Ошибка выполнения запроса: {error}")
            return []
        finally:
            cur.close()
            self.disconnect()  # Разрываем соединение

    def get_vacancies_with_higher_salary(self):
        '''Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''

        self.connect()  # Устанавливаем соединение
        if not self.conn:
            raise RuntimeError("Соединение не установлено.")

        cur = self.conn.cursor()
        query = """
            SELECT * FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies);
                """
        try:
            cur.execute(query)
            result = cur.fetchall()
            # return result
            result_list = []
            for (id_vacancy, name_vacancy, area, id_employer, name_employer, requirement, salary_from,
                 salary_to, url) in result:
                result_list.append(f"id_vacancy: {id_vacancy}, name_vacancy: {name_vacancy}, area: {area},"
                                   f"id_employer: {id_employer}, name_employer: {name_employer}, "
                                   f"requirement: {requirement}, salary_from: {salary_from}, "
                                   f"salary_to: {salary_to}, url: {url}")
            return result_list

        except Exception as error:
            print(f"Ошибка выполнения запроса: {error}")
            return []
        finally:
            cur.close()
            self.disconnect()  # Разрываем соединение

    def get_vacancies_with_keyword(self, keyword: str):
        '''Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова'''

        self.connect()  # Устанавливаем соединение
        if not self.conn:
            raise RuntimeError("Соединение не установлено.")

        cur = self.conn.cursor()
        query = """
            SELECT * FROM vacancies WHERE name_vacancy LIKE %s;
                """
        keyword_like = f"%{keyword}%"
        try:
            cur.execute(query, (keyword_like,))
            result = cur.fetchall()
            # return result
            result_list = []
            for (id_vacancy, name_vacancy, area, id_employer, name_employer, requirement, salary_from,
                 salary_to, url) in result:
                result_list.append(f"id_vacancy: {id_vacancy}, name_vacancy: {name_vacancy}, area: {area},"
                                   f"id_employer: {id_employer}, name_employer: {name_employer}, "
                                   f"requirement: {requirement}, salary_from: {salary_from}, "
                                   f"salary_to: {salary_to}, url: {url}")
            return result_list

        except Exception as error:
            print(f"Ошибка выполнения запроса: {error}")
            return []
        finally:
            cur.close()
            self.disconnect()  # Разрываем соединение


if __name__ == "__main__":
    # Получаем параметры для подключения к PostgresSQL
    params = config()
    # Записываем название базы данных
    database_name = 'base_vacancies'
    manager = DBManager(database_name, params)
    # Получаем список всех компаний и количество вакансий у каждой компании
    list_companies_and_vacancies_count = manager.get_companies_and_vacancies_count()
    print(list_companies_and_vacancies_count)
    # Получаем список всех вакансий с указанием названия компании, названия вакансии
    # и зарплаты и ссылки на вакансию
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

# Вариант с другим подключением к "base_vacancies" (название по умолчанию)
# class DBManager:
#     def __init__(self, database_name="base_vacancies"):
#         self.database_name = database_name
#         self.conn = None
#         self.params = config()
#
#     def connect(self):
#         try:
#             # Подключаемся к базе данных с параметрами из файла и именем базы данных
#             self.conn = psycopg2.connect(
#                 host=self.params['host'],
#                 database=self.database_name,
#                 user=self.params['user'],
#                 password=self.params['password']
#             )
#             print(f"Подключено к базе данных PostgreSQL: {self.database_name}")
#         except Exception as error:
#             print(f"Ошибка при подключении к PostgreSQL: {error}")
#
#     def disconnect(self):
#         if self.conn:
#             self.conn.close()
#             print(f"Отключено от базы данных PostgreSQL: {self.database_name}")
#
#     def get_all_vacancies(self):
#         self.connect()  # Устанавливаем соединение
#         if not self.conn:
#             raise RuntimeError("Соединение не установлено.")
#
#         cur = self.conn.cursor()
#         query = """
#             SELECT
#                 employers.name_employer,
#                 name_vacancy,
#                 salary_from,
#                 salary_to,
#                 vacancies_url
#             FROM
#                 employers
#             JOIN
#                 vacancies
#             ON
#                 employers.id_employer = vacancies.id_employer;
#         """
#         try:
#             cur.execute(query)
#             result = cur.fetchall()
#             # return result
#             vacancies_list = []
#             for name_employer, name_vacancy, salary_from, salary_to, vacancies_url in result:
#                 vacancies_list.append(f"name_employer: {name_employer}, name_vacancy: {name_vacancy},
#                 Salary: от {salary_from} до {salary_to}, vacancies_url: {vacancies_url}")
#             return vacancies_list
#
#         except Exception as error:
#             print(f"Ошибка выполнения запроса: {error}")
#             return []
#         finally:
#             cur.close()
#             self.disconnect()  # Разрываем соединение
#
#
# if __name__ == "__main__":
#     manager = DBManager()
#     vacancies = manager.get_all_vacancies()
#     for row in vacancies:
#         print(row)
