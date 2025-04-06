import requests


class HeadHunterApiVacancies:
    """Класс для работы с API HeadHunter, подключение к API и получение вакансий"""

    # Атрибуты экземпляра класса — приватные
    __url: str
    __params: dict
    __vacancies: list

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__params = {'text': '', 'search_field': 'name', 'employer_id': [], 'area': 113, 'period': 7,
                         'only_with_salary': True, 'per_page': 100, 'page': 0}
        self.__vacancies = []

    @property
    def url(self):
        return self.__url

    @property
    def params(self):
        return self.__params

    @property
    def vacancies(self):
        return self.__vacancies

    def _connect(self):
        """Метод подключения к API hh.ru и проверки статус-кода ответа."""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Запрос не выполнен с кодом состояния: {response.status_code}")
        return response.status_code

    @property
    def send_connect(self):
        return self._connect

    def get_vacancies(self, keyword: str = None, employers_id: list[str] = None):
        """Метод получает вакансии с возможностью поиска по ключевому слову и
        преобразует их, отбирая необходимые ключи со значениями"""

        self.params['text'] = keyword
        self.params['employer_id'] = employers_id
        if self.send_connect:
            while self.params.get('page') != 20:
                response = requests.get(self.url, params=self.params)
                data = response.json()['items']

                if len(data) == 0:
                    break  # Прекращаем цикл, если больше нет вакансий

                self.vacancies.extend(data)
                self.params['page'] += 1  # Переход на следующую страницу
        # return self.vacancies

        # Преобразуем список вакансий
        vacancies_result = []
        for vacancy in self.vacancies:
            vacancy_data = {
                'id_vacancy': vacancy['id'],
                'name_vacancy': vacancy['name'],
                'area': vacancy['area']['name'],
                'employer': vacancy['employer']['name'],
                'requirement': vacancy['snippet']['requirement'],
                'salary_from': vacancy['salary']['from'],  # if vacancy['salary']['from'] is not None else 0,
                'salary_to': vacancy['salary']['to'],  # if vacancy['salary']['to'] is not None else 0,
                'url': vacancy['url']
            }
            vacancies_result.append(vacancy_data)
        return vacancies_result

    # @staticmethod
    # def get_vacancies_selected_companies(vacancies_result, interesting_companies):
    #     '''Получаем список вакансий от интересующих нас компаний'''
    #
    #     vacancies_selected_companies = []
    #     for key in vacancies_result:
    #         if key['employer'] in interesting_companies:
    #             vacancies_selected_companies.append(key)
    #
    #     return vacancies_selected_companies


if __name__ == "__main__":
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterApiVacancies()
    # Проверяем прошел ли запрос успешно
    hh_connect = hh_api.send_connect()
    print(hh_connect)
    # Получение вакансий с hh.ru
    interesting_companies_id = ['11736287', '11774774', '11679140', '119162926', '9472604', '1978012', '906557', '9594816', '2870783', '5179890', '11282140', '6038553', '2265728', '1714677']
    hh_vacancies = hh_api.get_vacancies('', interesting_companies_id)  # ('Python') ['11736287', '6038553']
    print(hh_vacancies)
    print(type(hh_vacancies))
    print(len(hh_vacancies))


