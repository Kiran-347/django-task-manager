from django.urls import path
from . import views

urlpatterns= [
    path('', views.public_home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('toggle/<int:pk>/', views.toggle_complete, name = 'toggle_complete'),
    path('delete/<int:pk>/', views.delete_task,name='delete_task'),
    path('signup/',views.signup_view, name='signup'),
    ]