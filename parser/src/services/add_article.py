from articles.models import Article, ArticleCategory


def add_article(article_data):
    # Получаем или создаем категорию
    article_category, created = ArticleCategory.objects.get_or_create(name=article_data["category"])

    # Создаем новую статью
    article_model = Article(
        title=article_data["title"],
        information=article_data["text"],
        image=article_data["image"],
        category=article_category
    )

    # Удаляем самую старую статью, если превышен лимит
    if Article.objects.count() >= 275:
        oldest_article = Article.objects.order_by('id').first()
        if oldest_article:
            oldest_article.delete()

    article_model.save()
