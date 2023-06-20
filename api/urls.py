from django.urls import path
from . import views


urlpatterns = [
    path('news/', view=views.NewsCollectionView.as_view()),
    path('news/<int:pk>', view=views.SingleNewsView.as_view())
]