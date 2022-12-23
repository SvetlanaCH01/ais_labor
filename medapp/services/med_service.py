from ..serializers import ReceptionSerializer, DiagnosisSerializer, ClinicalGuideSerializer
from .repository_service import *


"""

    Данный модуль содержит программный слой с реализацией дополнительной бизнес-логики, 
    выполняемой перед или после выполнения операций над хранилищем данных (repository), 
    а также выполнение дополнительных операций над сериализаторами (если необходимо).

    ВАЖНО! Реализация данного слоя приведена в качестве демонстрации полной структуры RESTful веб-сервиса.
           В небольших проектах данный слой может быть избыточен, в таком случае, из контроллера ваших маршрутов 
           (Router в FastAPI или View в Django) можно напрямую работать с функциями хранилища данных (repository_service).
"""


class ReceptionService:

    def get_reception_for_diagnosis(self, diagnosis_id: int) -> Optional[ReceptionSerializer]:
        result = get_reception_by_diagnosis_id(diagnosis_id)
        if result is not None:
            return ReceptionSerializer(result)
        return result

    def get_all_reception_for_diagnosis(self, diagnosis_name: str) -> ReceptionSerializer:
        result = get_reception_by_diagnosis_name(diagnosis_name.upper())
        reception_data = ReceptionSerializer(result, many=True)     # для возвращения списка объектов, необходимо создание сериализатора с аргументом many=True
        return reception_data

    def add_reception_info(self, reception: ReceptionSerializer) -> None:
        reception_data = reception.data     # получаем валидированные с помощью сериализатора данные (метод .data  возвращает объект типа dict)
        create_reception(patient_id = reception_data.get('patient_id'),
                        doctor_id = reception_data.get('doctor_id'),
                        purpose = reception_data.get('purpose_of_visit'),
                        diagnosis_id = reception_data.get('diagnosis_id'),
                        guid = reception_data.get('clinical_guid'))

    def update_reception_info(self, reception: ClinicalGuideSerializer) -> None:
        reception_data = reception.data
        return update_reception_clinic_guide(diag_id = reception_data.get('diagnosis_id'),
                                            clinic_guid= reception_data.get('clinical_guid'))

        

    def delete_reception_info_by_diagnosis_id(self, diagnosis_id: int) -> None:
        delete_reception_by_diagnosis_id(diagnosis_id)

    def add_diagnos(self, diagnosis: DiagnosisSerializer) -> None:
        diagnos_data = diagnosis.data
        add_diagnos(diag_name=diagnos_data.get('name').upper())

