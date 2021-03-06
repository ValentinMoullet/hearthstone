from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^$',RedirectView.as_view(url=reverse_lazy('index'))),
	url(r'^index','handstats.views.index',name='index'),
	
	url(r'^initiate_game$','handstats.game.views.initiate_game',name='initiate_game'),
	url(r'^new_game$','handstats.game.views.new_game',name='new_game'),
	url(r'^end_turn$','handstats.game.views.end_turn',name='end_turn'),
	url(r'^use_opponent_card$','handstats.game.views.use_opponent_card',name='use_opponent_card'),
	url(r'^update_opponent_prob_maybe$','handstats.game.views.update_opponent_prob_maybe',name='update_opponent_prob_maybe'),
	url(r'^update_opponent_prob_sure$','handstats.game.views.update_opponent_prob_sure',name='update_opponent_prob_sure'),
	
	url(r'^existing_decks$','handstats.decks.views.existing_decks',name='existing_decks'),
	url(r'^create_deck$','handstats.decks.views.create_deck',name='create_deck'),
	url(r'^get_deck_list/(?P<deck_id>\d+)$','handstats.decks.views.get_deck_list',name='get_deck_list'),
	
	url(r'^get_matching_cards$','handstats.cards.views.get_matching_cards',name='get_matching_cards'),
	
	url(r'^create_new_deck_creation$','handstats.deck_creation.views.create_new_deck_creation',name='create_new_deck_creation'),
	url(r'^submit_deck_creation$','handstats.deck_creation.views.submit_deck_creation',name='submit_deck_creation'),
	url(r'^add_card_to_deck_creation$','handstats.deck_creation.views.add_card_to_deck_creation',name='add_card_to_deck_creation'),
	url(r'^remove_card_from_deck_creation$','handstats.deck_creation.views.remove_card_from_deck_creation',name='remove_card_from_deck_creation'),
	
	url(r'^help$','handstats.help.views.help',name='help'),
]