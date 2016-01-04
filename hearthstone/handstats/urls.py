from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^index/$','handstats.views.index',name='index'),
]