from django.urls import path 
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.lista_pacientes, name='lista'),
    path('<int:pk>/status/', views.mudar_status, name='mudar_status'),
    path('<int:pk>/alta/', views.dar_alta, name='em_alta'),
    path('<int:pk>/retorno/', views.retorno_paciente, name='retorno')
]