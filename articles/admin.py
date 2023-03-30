from django.contrib import admin
from articles.models import Appeal, Article, ArticleCategory

# Register your models here.
admin.site.register(Appeal)
admin.site.register(ArticleCategory)
admin.site.register(Article)
