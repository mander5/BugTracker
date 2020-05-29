from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('',views.TicketList.as_view(),name='all'),
    path('new/',views.CreateTicket.as_view(),name='create'),
    path('by/<username>/',views.UserTickets.as_view(),name='for_user'),
    path('by/<username>/<pk>/',views.TicketDetail.as_view(),name='single'),
    path('delete/<pk>/',views.DeleteTicket.as_view(),name='delete'),
]
