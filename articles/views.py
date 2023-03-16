from django.shortcuts import render, redirect
from articles.forms import AppealForm

# Create your views here.
def index(request):
    context={
        'title': "Главная | IT News"
    }
    return render(request,'articles/index.html',context=context)

def search(request):
    context={
        'title': "Поиск | IT News"
    }
    return render(request,'articles/search.html',context=context)

def article(request):
    context={
        'title': "Статья | IT News"
    }
    return render(request,'articles/article.html',context=context)

def category(request):
    context={
        'title': "Категории | IT News"
    }
    return render(request,'articles/category.html',context=context)

def contact(request):
    error = ""
    if request.method == 'POST':
        form=AppealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
        else:
            error="Некорректные данные"
    form = AppealForm()
    context={
        'title': "Контакты | IT News",
        'form': form,
        'error': error
    }
    return render(request,'articles/contact.html',context=context)
