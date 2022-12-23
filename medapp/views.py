from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status

from .serializers import ReceptionSerializer, DiagnosisSerializer, ClinicalGuideSerializer
from .services.med_service import ReceptionService

"""
    Данный модуль отвечает за обработку соответствующих HTTP операций.
    
    В рамках DRF возможны следующие реализации Django Views 
    (https://www.django-rest-framework.org/tutorial/2-requests-and-responses/):
    
    1. View на основе функций (function based views). Такие функции должны использовать декоратор @api_view.
    2. View на основе классов (class based views). Такие классы должны наследоваться от базовых классов типа APIView 
    (подробнее о class based views см.: https://www.django-rest-framework.org/api-guide/generic-views/).

"""


service = ReceptionService()      # подключаем слой с бизнес-логикой


class GetDelAllReception(GenericAPIView):
    serializer_class = ReceptionSerializer    # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]       # определяем тип входных данных

    def get(self, request: Request, diag_id: str) -> Response:
        """ Получение всех записей приема по диагнозу """
        response = service.get_reception_for_diagnosis(diag_id)
        return Response(data=response.data)

    def delete(self, request: Request, diag_id: int) -> Response:
        """ Удаление всех записей приема по диагнозу """
        service.delete_reception_info_by_diagnosis_id(int(diag_id))
        return Response(status=status.HTTP_200_OK)


class GetPostReception(GenericAPIView):
    serializer_class = ReceptionSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о приеме с поставленным диагнозом по идентификатору диагноза (необходим параметр ?diagnosis_id=) """
        diag_id = request.query_params.get('diagnosis_id')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?diagnosis_id=1
        if diag_id is None:
            return Response('Expecting query parameter ?diagnosis_id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_reception_for_diagnosis(int(diag_id))
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новую запись приема """
        serializer = ReceptionSerializer(data=request.data)
        if serializer.is_valid():
            service.add_reception_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PutReception(CreateAPIView):
    serializer_class = ClinicalGuideSerializer
    renderer_classes = [JSONRenderer]

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить самую старую запись о приеме с поставленным диагнозом по идентификатору диагноза (необходим параметр ?diagnosis_id=)"""
        serializer = ClinicalGuideSerializer(data=request.data)
        if serializer.is_valid():
            service.update_reception_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostDiagnosis(CreateAPIView):
    serializer_class = DiagnosisSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый диагноз """
        serializer = DiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            service.add_diagnos(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
