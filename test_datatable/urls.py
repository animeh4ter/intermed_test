from django.urls import path
from . import views

urlpatterns = [
    path('init_db/', views.init_db, name='init_db'),
    path('get_db_data/', views.get_db_data, name='api.get_db_data'),
    path('create_new/', views.create_new, name='api.create_new'),
]
