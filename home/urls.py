from django.urls import path
from .views import diagnosis,receptions,login,logout,\
    index,add_pacient,pacients,detail_pacient,\
    detail_diagnosis,add_receptions,detail_receptions,edit_receptions,remove_receptions,edit_pacient,remove_pacient

urlpatterns = [

    path('diagnosis/detail/<str:pk>',detail_diagnosis,name='detail_diagnosis'),
    path('diagnosis', diagnosis,name="diagnosis"),

    path('receptions/add', add_receptions,name="add_reception"),
    #path('receptions/edit/<str:pk>', edit_receptions,name="edit_reception"),
    #path('receptions/remove/<str:pk>', remove_receptions,name="remove_reception"),
    path('receptions/detail/<str:pk>', detail_receptions,name="detail_reception"),
    path('receptions', receptions,name="receptions"),

    path('pacients/add', add_pacient,name="add_pacient"),
    path('pacients/edit/<str:pk>', edit_pacient,name="edit_pacient"),
    path('pacients/remove/<str:pk>', remove_pacient,name="remove_pacient"),
    path('pacients/detail/<str:pk>', detail_pacient,name="detail_pacient"),
    path('pacients', pacients,name="pacients"),

    path('login', login,name="login"),
    path('logout', logout,name="logout"),
    path('', index,name="index")
]
