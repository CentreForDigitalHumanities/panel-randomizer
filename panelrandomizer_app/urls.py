from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('<str:name>/', views.index, name='index'),
    path('<str:name>/forward', views.forward, name='forward'),
]
