from django.urls import path

from articles.views import article, index, favourite, favourite_add, favourite_remove

app_name = "articles"

urlpatterns = [
    path('article/<int:article_number>/', article, name='article'),
    path('page/<int:page_number>/', index, name='paginator'),
    path('category/<int:category_number>/', index, name='category'),
    path('favourite/', favourite, name='favourite'),
    path('favourite/add/<int:article_number>/', favourite_add, name='favourite_add'),
    path('favourite/remove/<int:favourite_number>/', favourite_remove, name='favourite_remove'),
]
