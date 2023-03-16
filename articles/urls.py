from django.urls import path
from articles.views import article, category

urlpatterns = [
    path('article/', article, name='article'),
    path('category/', category, name='category'),
]
