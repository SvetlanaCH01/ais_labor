from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views

"""
    Подключение URI для приложения medapp.
    Корневые URI представлены в базовом модуле ais_lab/urls.py
"""

# Метаданные Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Clinical recommendations for broncho-pulmonary diseases API",
      default_version='v1',
      description="Clinical recommendations for broncho-pulmonary diseases API",
      terms_of_service="https://example.com",
      contact=openapi.Contact(email="contact@mail.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('clinicrecommend/<int:diag_id>', views.GetDelAllReception.as_view()),
    path('clinicrecommend', views.GetPostReception.as_view()),
    path('clinicrecommendchange', views.PutReception.as_view()),
    path('diagnosis', views.PostDiagnosis.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
