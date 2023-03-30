from django.urls import path
from articles.views import article, category, index

urlpatterns = [
    path('article/', article, name='article'),
    path('category/', category, name='category'),
    path('page/<int:page_number>', index, name='paginator'),
]
