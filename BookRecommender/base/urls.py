from django.urls import path
from . import views


urlpatterns = [
    path('',views.welcome),
    path('recommend/',views.recommend_ui),
    path('recommend_books', views.recommend_books, name='recommend_books')
]
