from django.urls import path
from . import views

urlpatterns = [    
    path('user_list/', views.user_list),
    path('reservation/', views.reservation_view, name = 'reservation'),
    path('chatbot/', views.chatbot, name='chatbot'),
]