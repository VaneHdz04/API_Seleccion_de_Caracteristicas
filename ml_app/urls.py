# ml_app/urls.py
from django.urls import path
from . import views

app_name = 'ml_app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('procesar/', views.procesar_view, name='procesar'),  # recibe POST con archivo y ejecuta
    path('resultados/<str:run_id>/', views.resultados_view, name='resultados'),
]
