from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_ems, name='login'),
    path('logout/', views.logout_ems, name='logout'),
]