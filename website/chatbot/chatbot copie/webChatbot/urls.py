from django.urls import path

from . import views

app_name = 'webChatbot'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ask', views.get_question, name='ask'),
]