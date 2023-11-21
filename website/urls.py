from . import views
from django.urls import path

urlpatterns = [
    path('', views.GameListView.as_view(), name='home')  
]
