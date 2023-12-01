# urls.py
from django.urls import path
from .views import create_user, accept, terms, get_question_form, get_result, end, speech_to_text, get_report

urlpatterns = [
    path('', create_user, name='app_mbti/index.html'),
    path('aceptar/<int:user_id>/', accept, name='aceptar'),
    path('terminos/<int:user_id>/', terms, name='terminos'),   
    path('preguntas/<int:user_id>/<int:question_id>/', get_question_form, name='get_question_form'),
    path('resultado/<int:user_id>/', get_result, name='resultado'),
    path('fin/<int:user_id>/', end, name='fin'),
    path('audio/<int:user_id>/<int:question_id>/', speech_to_text, name='audio'),
    path('reporte/<int:user_id>', get_report, name='reporte'),
]
