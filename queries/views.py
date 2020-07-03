from django.shortcuts import render

from . import forms
from . import models

TEMPLATE_FILENAME = 'index.html'


def get_query(request):
    if request.method == 'POST':
        form = forms.QueryForm(request.POST)
        if form.is_valid():
            ip_address = request.META.get('REMOTE_ADDR')
            result = models.QueryResult.objects.get_or_create(user_ip=ip_address, phrase=request.POST['phrase'])
            context = {'form': form, 'links': result.link_set.order_by('position').all()}
            return render(request, TEMPLATE_FILENAME, context)

    return render(request, TEMPLATE_FILENAME, {'form': forms.QueryForm()})
