from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),  
    path('game/<int:pk>/review/', views.UserReviewsView.as_view(), name='review_game'),
]
