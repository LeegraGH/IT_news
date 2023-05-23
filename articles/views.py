from django.shortcuts import render, redirect
from articles.forms import AppealForm
from django.core.paginator import Paginator
from articles.models import Article
from src import parse_news
from bs4 import BeautifulSoup
import requests


# Create your views here.


def index(request, page_number=1):
    parse_news.parser()
    articles = Article.objects.all().order_by('-id')
    paginator = Paginator(articles, per_page=11)
    articles_paginator = paginator.page(page_number)
    context = {
        'title': "Главная | IT News",
        'articles': articles_paginator,
        'paginator_range': list(paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)),
        'popular_articles': articles[:3]
    }
    return render(request, 'articles/index.html', context=context)


def search(request):
    context = {
        'title': "Поиск | IT News"
    }
    return render(request, 'articles/search.html', context=context)

def group(request):
    context = {
        'title': "О нас | IT News"
    }
    return render(request, 'articles/group.html', context=context)

def article(request, article_number):
    parse_news.parser()
    all_text = []
    image = ""
    articles = Article.objects.all().order_by('-id')
    context = {
        'title': "Статья | IT News",
        'popular_articles': articles[:3]
    }
    article_data = Article.objects.get(id=article_number)
    previous_article = None
    next_article = None
    if Article.objects.filter(id=article_number - 1).exists():
        previous_article = Article.objects.get(id=article_number - 1)
    if Article.objects.filter(id=article_number + 1).exists():
        next_article = Article.objects.get(id=article_number + 1)
    try:
        page = requests.get("https://www.igromania.ru" + article_data.url)
        soup = BeautifulSoup(page.text, "html.parser")
        info = soup.find("div", {"class": "universal_content"}).find_all(["div","ol","ul"], {"class": []})[:-1]
        image = soup.find("div", {"class": "main_pic_container"}).find_next("img")["src"]
        for div_text in info:
            if div_text.find("div", {"class": ["sign_container","grayblock_nom"]}) is not None:
                continue
            text = div_text.text.strip()
            if div_text.find("div", {"class": "uninote console"}) is not None:
                break
            # if "Больше на Игромании" in text:
            #     break
            if text != "":
                all_text.append(text)
    except Exception as e:
        print(e)
    finally:
        context["article"] = article_data
        context["all_text"] = all_text
        context["image"] = image
        context["previous"] = previous_article
        context["next"] = next_article
        return render(request, 'articles/article.html', context=context)


def category(request):
    context = {
        'title': "Категории | IT News"
    }
    return render(request, 'articles/category.html', context=context)


def contact(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    form = AppealForm()
    context = {
        'title': "Контакты | IT News",
        'form': form
    }
    return render(request, 'articles/contact.html', context=context)
