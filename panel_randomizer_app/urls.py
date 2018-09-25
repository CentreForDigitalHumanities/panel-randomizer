from django.urls import path

from . import views

urlpatterns = [
    path('', views.url_invalid, name='url_invalid'),
    path('<str:name>/', views.index, name='index'),
    path('<str:name>/participate', views.participate, name='participate'),
]
