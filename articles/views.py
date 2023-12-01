from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from articles.forms import AppealForm, MailForm
from articles.models import Article

from parser.src.parsers.habr_parser import habr_parse

# Create your views here.


def index(request, page_number=1):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = MailForm()

    # mail_parse()
    # habr_parse()


    articles = Article.objects.all().order_by('-id')
    paginator = Paginator(articles, per_page=11)
    articles_paginator = paginator.page(page_number)
    context = {
        'title': "Главная | IT News",
        'articles': articles_paginator,
        'paginator_range': list(paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)),
        'popular_articles': articles[:3],
        'form': form
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
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article', article_number=article_number)
    form = MailForm()

    articles = Article.objects.all().order_by('-id')
    context = {
        'title': "Статья | IT News",
        'popular_articles': articles[:3],
        'form': form
    }
    article_data = Article.objects.get(id=article_number)
    previous_article = None
    next_article = None
    if Article.objects.filter(id=article_number - 1).exists():
        previous_article = Article.objects.get(id=article_number - 1)
    if Article.objects.filter(id=article_number + 1).exists():
        next_article = Article.objects.get(id=article_number + 1)

    context["article"] = article_data
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
