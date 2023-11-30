from django.db import models


# Create your models here.
class Appeal(models.Model):
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=75)
    message = models.TextField()

    def __str__(self):
        return f"{self.username}: {self.email}"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"


class Mailing(models.Model):
    email = models.CharField(max_length=75)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылка"


class ArticleCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(max_length=50, unique=True)
    # description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Класс, который представляет модель для хранения информации о статьях в БД
    """

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    title = models.CharField(max_length=150)
    description = models.TextField()
    information = models.TextField()
    image = models.ImageField(upload_to="articles_images", null=True, blank=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=ArticleCategory, on_delete=models.PROTECT)

    def __str__(self):
        return f'Статья: {self.title} | Категория: {self.category}'
