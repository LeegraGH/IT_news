from bs4 import BeautifulSoup
import requests
from articles.models import Article, ArticleCategory
from django.core.exceptions import ObjectDoesNotExist

def parser():
    page = requests.get("https://www.igromania.ru/news/")
    soup = BeautifulSoup(page.text, "html.parser")
    articles = soup.find_all("div", {"class": "aubl_item"})

    for article in articles:
        # date = article.find_next("div", {"class": "aubli_date"}).text
        article_data = {
            "url": article.find_next("a", {"class": "aubli_name"}).get("href"),
            "name": article.find_next("a", {"class": "aubli_name"}).text,
            "desc": article.find_next("div", {"class": "aubli_desc"}).text,
            "category": article.find_next("div", {"class": "aubli_sect"}).text,
        }
        article_category = ArticleCategory(name=article_data["category"])
        try:
            category_clone=ArticleCategory.objects.get(name=article_category.name)
        except ObjectDoesNotExist:
            article_category.save()
        article_model = Article(
            name=article_data["name"],
            url = article_data["url"],
            description =article_data["desc"],
            # information =article_data["name"],
            category = ArticleCategory.objects.get(name=article_category.name)
        )
        try:
            article_clone=Article.objects.get(name=article_model.name)
        except ObjectDoesNotExist:
            article_model.save()
