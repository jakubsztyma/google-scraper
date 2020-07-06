import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import status

from . import forms, utils
from . import models

TEMPLATE_FILENAME = 'index.html'


@require_http_methods(["GET", "POST"])
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


@require_http_methods(["GET"])
def proxy(request, phrase):
    if request.method == 'GET':
        data = utils.get_response_from_google(phrase)
        return HttpResponse(json.dumps(data))

    return HttpResponse("Please provide 'phrase' parameter", status=status.HTTP_400_BAD_REQUEST)
