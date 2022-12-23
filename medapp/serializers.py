from rest_framework import serializers


"""
    В данном модуле реализуются сериализаторы DRF, позволяющие 
    валидировать данные для моделей DAO (models.py), 
    а также сериализующие (преобразующие) эти модели в стандартные 
    объекты Python (dict) и в формат json. Подробнее см.: 
    https://www.django-rest-framework.org/api-guide/serializers/
    https://www.django-rest-framework.org/api-guide/fields/
    
    Сериализаторы DRF являются аналогом DTO для Django. 
"""


class ReceptionSerializer(serializers.Serializer):

    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    purpose_of_visit = serializers.CharField()
    diagnosis_id = serializers.IntegerField()
    clinical_guid = serializers.CharField()
    updated_on = serializers.DateTimeField(required=False)# объявление необязательного поля (may be None)

    """ Класс Serializer позволяет переопределить наследуемые 
        методы create() и update(), в которых, например, можно реализовать бизнес-логику 
        для сохранения или обновления валидируемого объекта (например, для DAO ) """

class ClinicalGuideSerializer(serializers.Serializer):

    diagnosis_id = serializers.IntegerField()
    clinical_guid = serializers.CharField()
    updated_on = serializers.DateTimeField(required=False)# объявление необязательного поля (may be None)

    """ Класс Serializer позволяет переопределить наследуемые 
        методы create() и update(), в которых, например, можно реализовать бизнес-логику 
        для сохранения или обновления валидируемого объекта (например, для DAO ) """


class DiagnosisSerializer(serializers.Serializer):
    name = serializers.CharField()
