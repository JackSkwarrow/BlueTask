from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("delete-record/", views.delete_record, name='delete_record'),
    path("add-record/", views.add_record, name='add_record'),
    path("reload-table/", views.reload_table, name='reload_table'),
]   
