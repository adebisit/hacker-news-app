from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.latest_news, name='latest-news'),
    path('news/<int:item_id>/', views.news_details, name='news_details')
]