from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote, name='random_quote'),
    path('like/<int:quote_id>/', views.like_quote, name='like_quote'),
    path('dislike/<int:quote_id>/', views.dislike_quote, name='dislike_quote'),
    path('add/', views.add_quote, name='add_quote'),
    path('add/source/', views.add_source, name='add_source'),
    path('top/', views.top_quotes, name='top_quotes'),
]