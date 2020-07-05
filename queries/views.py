from django.shortcuts import render

from . import forms
from . import models

TEMPLATE_FILENAME = 'index.html'


def index(request):
    if request.method == 'POST':
        form = forms.QueryForm(request.POST)
        if form.is_valid():
            result = models.QueryResult.objects.get_or_create(
                user_ip=request.META.get('REMOTE_ADDR'),
                user_browser=request.META.get('HTTP_USER_AGENT', ''),
                phrase=form.cleaned_data['phrase']
            )
            context = {
                'form': form,
                'result': result,
                'links': result.link_set.order_by('-position').all(),
                'popular_words': result.popularword_set.order_by('-position').all(),
            }
            return render(request, TEMPLATE_FILENAME, context)

    return render(request, TEMPLATE_FILENAME, {'form': forms.QueryForm()})
