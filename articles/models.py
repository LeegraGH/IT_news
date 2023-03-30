from django.db import models


# Create your models here.
class Appeal(models.Model):
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{self.username}: {self.email}"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"


class ArticleCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    # information = models.TextField()
    category = models.ForeignKey(to=ArticleCategory, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add = True)
    date = models.DateField(auto_now_add = True)
    # auto_now_add = True

    def __str__(self):
        return f'Статья: {self.name} | Категория: {self.category}'
