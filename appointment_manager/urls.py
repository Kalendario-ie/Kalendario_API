
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('scheduling.urls')),
    url(r'^.*', TemplateView.as_view(template_name="home.html"), name="home")

]
