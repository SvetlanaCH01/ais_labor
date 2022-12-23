from typing import Optional, Iterable, List
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import Doctor, Patient, Diagnosis, Reception

"""

    Данный модуль является промежуточным слоем приложения, который отделяет операции 
    для работы с моделями DAO от основной бизнес-логики приложения. Создание данного 
    слоя позволяет унифицировать функции работы с источником данных, и, например, если 
    в приложении нужно будет использовать другой framework для работы с БД, вы можете 
    создать новый модуль (repository_service_newframework.py) и реализовать в нем функции 
    с аналогичными названиями (get_reception_by_diagnosis_id, и т.д.). Новый модуль можно будет
    просто импортировать в модуль с основной бизнес-логикой, практически не меняя при этом
    остальной код.
    Также отделение функций работы с БД можно сделать через отдельный абстрактный класс и 
    использовать порождающий паттерн для переключения между необходимыми реализацииями.

"""

def get_reception_by_diagnosis_id(diag_id: int) -> Optional[Reception]:
    """ Выборка одной записи приема по идентификатору (PrimaryKey) диагноза """
    reception = Reception.objects.filter(diagnosis__id=diag_id).order_by('updated_on').first()
    # из объекта Reception мы можем получить объекты Diagnosis, Doctor и Patient через вызов:
    # Reception.diagnosis
    # Reception.patient
    # Reception.doctor
    # ВАЖНО! Каждый такой вызов будет запускать отдельный SQL-запрос в БД
    return reception


def get_reception_by_diagnosis_name(diag_name: str) -> QuerySet:
    """ Выборка всех приемов по наименованию диагноза """
    reception = Reception.objects.select_related('diagnosis').filter(diagnosis__name=diag_name).all()
    # объект Reception и связанные объекты Diagnosis (сфильтром по diag_name) будут получены
    # через JOIN-запрос, т.о. при вызове Reception.diagnosis дополнительных SQL-запросов не будет
    # Конструкция diag__name означает обращение к полю "name" объекта Diagnosis, связанного с Reception через поле "diagnosis"
    return reception


def create_reception(patient_id: id, doctor_id: id, purpose: str, diagnosis_id: int, guid: str) -> None:
    """ Создание нового объекта Reception и добавление записи о погоде """
    reception  = Reception.objects.create(
        patient_id= patient_id,
        doctor_id=doctor_id,
        purpose_of_visit=purpose,
        diagnosis_id= diagnosis_id,
        clinical_guid= guid
    )
    reception.save()


def update_reception_clinic_guide(diag_id: int, clinic_guid:str) -> None:
    """ Обновление клинических рекомендаций для заданного диагноза (самой старой записи  для заданного диагноза)"""
    reception = get_reception_by_diagnosis_id(diag_id)
    reception.clinical_guid = clinic_guid
    reception.save()


def delete_reception_by_diagnosis_name(diag_name: str) -> None:
    """ Удаление записей приема по указанному названию диагноза """
    get_reception_by_diagnosis_name(diag_name).delete()

def delete_reception_by_diagnosis_id(diag_id: int) -> None:
    """ Удаление записей приема по указанному номеру диагноза """
    get_reception_by_diagnosis_id(diag_id).delete()

def add_diagnos(diag_name: str) -> None:
    """ Добавление нового диагноза """
    diag = Diagnosis.objects.create(name=diag_name)
    diag.save()

def add_patient(surname: str, name:str, patronymic:str, date_birth:str, passport_id:int, address:str,  phone_number:int) -> None:
    """ Добавление нового пациента """
    patient= Patient.objects.create(surname=surname, name= name, patronymic= patronymic,passport_ID = passport_id,date_of_birth = date_birth, address= address,phone_number= phone_number)
    patient.save()
