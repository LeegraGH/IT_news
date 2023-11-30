import re

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from articles.models import Article, ArticleCategory


# @app.task(name='parse_data', bind=True)
@shared_task
def parse_data():
    habr_parse()
    mail_parse()
    return True


@shared_task
def mail_parse():
    try:
        site_url = 'https://hi-tech.mail.ru/category/technology/'
        html = requests.get(site_url)

        soup = BeautifulSoup(html.text, 'html.parser')
        articles = soup.find_all('div',
                                 {'data-qa': 'ArticleThumb'})
    except:
        print("Error: Could not parse Hi-Tech Mail!")
        return

    for article in articles:
        try:
            article_url = 'https://hi-tech.mail.ru' + article.find(
                lambda tag: tag.name == 'div' and tag.get('data-qa') in ['Text', 'Title']).find("a").get("href")

            title = article.find(
                lambda tag: tag.name == 'div' and tag.get('data-qa') in ['Text', 'Title']).text.replace(u'\xa0',
                                                                                                        u' ')

            image = ""
            try:
                image = article.find("picture", {'data-qa': 'Picture'}).find('img').get("src")
            except:
                pass

            article_data = {
                "category": "hi-tech Mail.ru",
                "title": title,
                "image": image,
                "text": ""
            }

            article_html = requests.get(article_url)

            article_soup = BeautifulSoup(article_html.text, 'html.parser')

            article_text = article_soup.find('main', {'data-qa': 'ArticleLayout'}).find_all('div', {
                'article-item-type': 'html'})

            for block in article_text:
                text_array = block.find_all('p')

                for part in text_array:
                    article_data["text"] += part.get_text().replace(u'\xa0', u' ') + " "

            add_article(article_data)
            print(article_data)

        except:
            continue


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
