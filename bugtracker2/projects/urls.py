from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('',views.ListProject.as_view(),name='all'),
    path('new/', views.CreateProject.as_view(), name='create'),
    path('ticket/in/<slug>/', views.SingleProject.as_view(),name='single'),
    path('join/<slug>/', views.JoinProject.as_view(),name='join'),
    path('leave/<slug>/', views.LeaveProject.as_view(),name='leave'),
]
