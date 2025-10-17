from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('list/', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('export/', views.export_csv, name='export_csv'),
]
