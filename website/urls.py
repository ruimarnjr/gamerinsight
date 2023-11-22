from . import views
from django.urls import path

urlpatterns = [
    path('', views.GameListView.as_view(), name='home'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),  
]
