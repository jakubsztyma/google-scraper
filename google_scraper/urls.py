from django.conf.urls import url
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^doc/', get_swagger_view(title='Documentation')),
]
