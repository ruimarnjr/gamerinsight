from . import views
from .views import GameCollection
from .views import GameDetailView
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('gamecollection/', GameCollection.as_view(), name='game_collection'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
]
