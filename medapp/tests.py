from django.test import TestCase
import random
from .services.repository_service import *


"""
   Данный модуль реализует "тестовые случаи/ситуации" для модуля repository_service.
   Для создания "тестового случая" необходимо создать отдельный класс, который наследует 
   базовый класс TestCase. Класс django.test.TestCase является подклассом unittest.TestCase 
   стандартного Python модуля для тестирования - unittest.

   Более детально см.: https://docs.djangoproject.com/en/4.1/topics/testing/overview/
"""

# Create your tests here.
class TestMedicalRepositoryService(TestCase):
    """ Все тестовые методы в классе TestCase (по соглашению)
        должны начинаться с префикса test_* """

    def setUp(self):
        """ Наследуемый метод setUp определяет инструкции,
            которые должны быть выполнены ПЕРЕД тестированием """
        # создаем тестовые записи
        add_diagnos('COVID-19') 
        add_patient(surname='Пугачев',name= 'Николай', patronymic='Артемович', date_birth='1999-09-08', passport_id=4657382948, address='г. Уфа, ул. Мубарякова, д.3, кв. 10', phone_number=89173645364) 


    def test_get_reception(self):
        """ Тест функции поиска записи  по диагнозу"""
        reception_in_bronhit_rows = get_reception_by_diagnosis_name('COVID-19')
        for row in reception_in_bronhit_rows:
            print(row)
            self.assertIsNotNone(row)  # запись должна существовать
            self.assertTrue(row.diag_id == 1)  # идентификатор diag_id == 1 (т.е. диагноз COVID-19 в таблице Diagnosis)
            self.assertTrue(row.diagnosis.name == 'COVID-19')  # проверка связи по FK

    def test_delete_reception(self):
        """ Тест функции удаления записи Reception по наименованию диагноза """
        delete_reception_by_diagnosis_name(diag_name='COVID-19')
        result =get_reception_by_diagnosis_id(diag_id=1)  # ищем запись по идентификатору диагноза COVID-19
        self.assertIsNone(result)  # запись не должна существовать
    
    def tearDown(self):
        """ Наследуемый метод tearDown определяет инструкции,
            которые должны быть выполнены ПОСЛЕ тестирования """
        pass