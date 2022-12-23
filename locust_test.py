import json
import time
import random
import json
from locust import HttpUser, task, tag, between


# Статичные данные для тестирования
#DIAGNOSIS_NAMES = ['Бронхит', 'Пневмония', 'Трахеит', 'Аллергоз']


class RESTServerUser(HttpUser):
    """ Класс, эмулирующий пользователя / клиента сервера """
    wait_time = between(1.0, 5.0)       # время ожидания пользователя перед выполнением новой task

    # Адрес, к которому клиенты (предположительно) обращаются в первую очередь (это может быть индексная страница, страница авторизации и т.п.)
    #def on_start(self):
     #   self.client.get("/docs")    # базовый класс HttpUser имеет встроенный HTTP-клиент для выполнения запросов (self.client)

    @tag("get_one1_task")
    @task(3)
    def get_one1_task(self):
        """ Тест GET-запроса (получение записи о диагнозе) """
        diag_id = random.randint(1, 8)      # генерируем случайный id в диапазоне [1, 8]
        with self.client.get(f'/api/clinicrecommend/{diag_id}',
                             catch_response=True,
                             name='/api/clinicrecommend/{diag_id}') as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            # Иначе обозначаем как "отказ"
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("get_one2_task")
    @task(10)
    def get_one2_task(self):
        """ Тест GET-запроса (получение одной записи о диагнозе) """
        diag_id = random.randint(1, 8)
        with self.client.get(f'/api/clinicrecommend?diagnosis_id={diag_id}',
                             catch_response=True,
                             name='/api/clinicrecommend?diagnosis_id={ID}') as response:
            # Если получаем код HTTP-код 200 или 204, то оцениваем запрос как "успешный"
            if response.status_code == 200 or response.status_code == 204:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("post_task")
    @task(1)
    def post_task(self):
        """ Тест POST-запроса (создание записи о погоде) """
        # Генерируем случайные данные в опредленном диапазоне
        test_data = {'patient_id': random.randint(1, 3),
                     'doctor_id': random.randint(1, 3),
                     'purpose_of_visit': "Консультация",
                     'diagnosis_id': random.randint(1, 8),
                     'clinical_guid': "Рекомендация ..."}
        post_data = json.dumps(test_data)       # сериализуем тестовые данные в json-строку
        # отправляем POST-запрос с данными (POST_DATA) на адрес <SERVER>/api/clinicrecommend
        with self.client.post('/api/clinicrecommend',
                              catch_response=True,
                              name='/api/clinicrecommend', data=post_data,
                              headers={'content-type': 'application/json'}) as response:
            # проверяем, корректность возвращаемого HTTP-кода
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("put_task")
    @task(3)
    def put_task(self):
        """ Тест PUT-запроса (обновление записи о приеме) """
        diag_id = random.randint(2, 4)  # генерируем случайный id в диапазоне [2, 4]
        test_data = {'diagnosis_id': diag_id,
                     'clinical_guid': "Клиническая рекомендация для {diag_id}"}
        put_data = json.dumps(test_data)
        # отправляем PUT-запрос на адрес <SERVER>/api/clinicrecommendchange
        with self.client.put('/api/clinicrecommendchange',
                             catch_response=True,
                             name='/api/clinicrecommendchange',
                             data=put_data,
                             headers={'content-type': 'application/json'}) as response:
            if response.status_code == 202:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

