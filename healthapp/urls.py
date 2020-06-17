from django.urls import path

from healthapp.views import predict

urlpatterns = [
    path('', predict.index, name='index'),
    path('main/', predict.main_symptom, name='main'),
    path('related/', predict.process_symptoms, name='related'),
    path('result/', predict.result_view, name='result'),
    path('another/', predict.predict_another, name='another'),
]