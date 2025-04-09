import requests


class HeadHunterApiEmployers:
    """Класс для работы с API HeadHunter, подключение к API и поиск работодателя"""

    # Атрибуты экземпляра класса — приватные
    __url: str
    __params: dict
    __vacancies: list

    def __init__(self):
        self.__url = 'https://api.hh.ru/employers'
        self.__params = {'text': '', 'area': 113, 'only_with_vacancies': True, 'per_page': 100, 'page': 0}
        self.__employers = []

    @property
    def url(self):
        return self.__url

    @property
    def params(self):
        return self.__params

    @property
    def employers(self):
        return self.__employers

    def _connect(self):
        """Метод подключения к API hh.ru и проверки статус-кода ответа."""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Запрос не выполнен с кодом состояния: {response.status_code}")
        return response.status_code

    @property
    def send_connect(self):
        return self._connect

    def reset_state(self):
        """Метод для сброса состояния объекта перед новым запросом."""
        self.__employers.clear()
        self.__params['text'] = ''
        self.__params['page'] = 0

    def get_employers(self, keyword=None):
        """Метод получает вакансии с возможностью поиска по ключевому слову и
        преобразует их, отбирая необходимые ключи со значениями"""

        self.reset_state()  # Сбрасываем состояние перед новым запросом
        self.params['text'] = keyword
        if self.send_connect:
            while self.params.get('page') != 50:
                response = requests.get(self.url, params=self.params)
                data = response.json()['items']

                if len(data) == 0:
                    break  # Прекращаем цикл, если больше нет вакансий

                self.employers.extend(data)
                self.params['page'] += 1  # Переход на следующую страницу
        # return self.employers

        # Преобразуем вывод работодателя
        employers_result = []
        for employer in self.employers:
            employer_data = {
                'id_employer': employer['id'],
                'name_employer': employer['name'],
                'url_employer': employer['url'],
                'vacancies_url': employer['vacancies_url'],
                'open_vacancies': employer['open_vacancies']
            }
            employers_result.append(employer_data)
        return employers_result


if __name__ == "__main__":
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterApiEmployers()
    # Проверяем прошел ли запрос успешно
    hh_connect = hh_api.send_connect()
    print(hh_connect)
    # Получение компании с hh.ru по ее названию
    # hh_employers = hh_api.get_employers('Tech Horizon')
    # print(hh_employers)

    interesting_companies = ['Tech Horizon', 'Кадровое агентство HireWay', 'Project Brain', 'Аптрейд',
                             'Кадровое агентство Candidate', 'ВижнЛабс VisionLabs', 'SberTech', 'Wildbox',
                             'LATOKEN', 'Enjoypro', 'RecruitTech', 'Таубина Софья Антоновна',
                             'Джем-Софт', 'kt.team']

    # # Получение списка отобранных компаний с hh.ru по списку их названий
    list_interesting_companies = []
    for company in interesting_companies:
        # В цикле получаем каждое название компании, передаем в метод класса и записываем в переменную
        hh_employers = hh_api.get_employers(company)
        # Полученный результат в переменной добавляем в список
        list_interesting_companies.extend(hh_employers)

    print(list_interesting_companies)
    print(len(list_interesting_companies))
