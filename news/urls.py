from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.latest_news, name='latest-news'),
    path('news/<int:pk>/', views.news_details, name='news_details'),
    path('subitems/<int:pk>', views.get_sub_items, name='sub_items')
]