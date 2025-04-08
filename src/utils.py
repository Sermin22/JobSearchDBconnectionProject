import psycopg2
from typing import Any


def create_database(database_name: str, params: dict) -> None:
    """Функция обеспечивает подключение PostgresSQL и создает базу данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

def create_table(database_name: str, params: dict) -> None:
    """Функция обеспечивает подключение к базе данных и создает таблицы"""

    # Подключаемся к базе данных с параметрами из файла и именем базы данных
    conn = psycopg2.connect(dbname=database_name, **params)

    # Создаем таблицу employers
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS employers")
        cur.execute("""
                CREATE TABLE employers (
                    id_employer VARCHAR(50) PRIMARY KEY,
                    name_employer VARCHAR(300) NOT NULL,
                    url_employer TEXT,
                    vacancies_url TEXT,
                    open_vacancies INT
                )
            """)

    # Создаем таблицу vacancies
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS vacancies")
        cur.execute("""
                CREATE TABLE vacancies (
                    id_vacancy VARCHAR(50) PRIMARY KEY,
                    name_vacancy VARCHAR(300) NOT NULL,
                    area VARCHAR(100),
                    id_employer VARCHAR(50),
                    name_employer VARCHAR(300) NOT NULL,
                    requirement TEXT,
                    salary_from INT,
                    salary_to INT,
                    url TEXT,
                    
                    CONSTRAINT fk_vacancies_id_employer FOREIGN KEY (id_employer) REFERENCES employers(id_employer)
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(data_employers: list[dict[str, Any]], data_vacancies: list[dict[str, Any]],
                          database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных"""

    # Устанавливаем соединение с базой
    conn = psycopg2.connect(dbname=database_name, **params)

    # Создаем курсор и записываем данные в таблицы
    with conn.cursor() as cur:
        # Записываем данные в таблицу employers
        for employer in data_employers:
            cur.execute(
                """
                INSERT INTO employers (id_employer, name_employer, url_employer, vacancies_url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (employer['id_employer'], employer['name_employer'], employer['url_employer'],
                 employer['vacancies_url'], employer['open_vacancies'])
            )

        # Записываем данные в таблицу vacancies
        for vacancy in data_vacancies:
            cur.execute(
                """
                INSERT INTO vacancies (id_vacancy, name_vacancy, area, id_employer, name_employer,
                requirement, salary_from, salary_to, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id_vacancy'], vacancy['name_vacancy'], vacancy['area'],
                 vacancy['id_employer'], vacancy['name_employer'], vacancy['requirement'], vacancy['salary_from'],
                 vacancy['salary_to'], vacancy['url'])
            )

    conn.commit()
    conn.close()