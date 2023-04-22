from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [    
    path('user_list/', views.user_list),
    path('reservation/', views.reservation_view, name = 'reservation'),
    path('chatbot/', views.chatbot, name='chatbot'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)