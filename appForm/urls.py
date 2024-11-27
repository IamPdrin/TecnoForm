from django.urls import path 
from . import views
path('add_cep/', views.add_cep, name='add_cep'),


urlpatterns = [
    path('', views.appForm, name="appForm"),
    path('excluir/<int:id_cep>', views.excluir_cep, name="excluir_cep"),
    path('adicionar', views.add_cep, name="add_cep"),
    path('editar/<int:id_cep>', views.editar_cep, name="editar_cep"),
]