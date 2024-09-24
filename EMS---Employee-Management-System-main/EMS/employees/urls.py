from django.urls import path, include
from . import views

urlpatterns = [
    path('add_employee/', views.add_employee, name='add_employee'),
    path('home/', views.home, name='home'),
    path('delete_employee/<int:pk>', views.delete_employee, name='delete_employee'),
    path('edit_employee/<int:pk>', views.edit_employee, name='edit_employee'),
]
