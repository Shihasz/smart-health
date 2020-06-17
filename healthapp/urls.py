from django.urls import path

from healthapp.views import predict

urlpatterns = [
    path('', predict.index, name='index'),
    path('/main', predict.main, name='main'),
]