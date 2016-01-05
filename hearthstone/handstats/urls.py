from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^$',RedirectView.as_view(url=reverse_lazy('index'))),
	url(r'^index$','handstats.views.index',name='index'),
	url(r'^initiate_game$','handstats.game.views.initiate_game',name='initiate_game'),
	url(r'^existing_decks$','handstats.decks.views.existing_decks',name='existing_decks'),
	url(r'^create_deck$','handstats.decks.views.create_deck',name='create_deck'),
	url(r'^help$','handstats.help.views.help',name='help'),
]