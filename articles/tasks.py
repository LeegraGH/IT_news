from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import app, shared_task

import requests
from bs4 import BeautifulSoup

from articles.models import Article, ArticleCategory


@shared_task
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


# функция скрапинга
@shared_task
def habr_parse():
    try:
        site_url = 'https://habr.com/ru/news/'
        html = requests.get(site_url)

        soup = BeautifulSoup(html.text, 'html.parser')
        articles = soup.find_all('article',
                                 {'class': 'tm-articles-list__item'})
    except:
        print("Error: Could not parse Habr!")
        return

    for article in articles:
        try:
            article_url = 'https://habr.com' + article.find("a", {"class": "tm-title__link"}).get("href")

            title = article.find("a", {"class": "tm-title__link"}).find("span").text.replace(u'\xa0', u' ')

            image = ""
            try:
                image = article.find(lambda tag: tag.name == "img" and (
                        not tag.get("class") or "tm-article-snippet__lead-image" in tag.get("class"))).get(
                    "src")
            except:
                pass

            # descr = re.sub(r'  +', ' ',
            #                article.find("div", {"class": "article-formatted-body"}).text.replace(u'\xa0', u' '))

            article_data = {
                "category": "Habr",
                "title": title,
                "image": "",
                # "descr": descr,
                "text": ""
            }

            article_html = requests.get(article_url)

            article_soup = BeautifulSoup(article_html.text, 'html.parser')
            try:
                article_image = article_soup.find('figure', {'class': 'full-width'}).find('img').get(
                    'src') if image == "" else image
                article_data["image"] = article_image
            except:
                pass

            article_text = article_soup.find('div', {'class': 'article-formatted-body'}).get_text()

            cleaned_text = article_text.replace(u'\xa0', u' ')
            # formatted_text = re.sub(r'(?<![\w\d])\.([^\s])', r'.\n\1', cleaned_text)
            formatted_text = re.sub(r'(?<![\w\d])\.([^\s])', r'. \1', cleaned_text)
            formatted_text = re.sub(r'  +', ' ', formatted_text)
            article_data["text"] = formatted_text

            add_article(article_data)
            print(article_data)

        except:
            continue
