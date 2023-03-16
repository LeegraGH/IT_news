from django.shortcuts import render


def page_not_found_view(request, exception):
    context = {
        'return_path': request.META.get('HTTP_REFERER', '/')
    }
    return render(request, '404.html', status=404, context=context)
