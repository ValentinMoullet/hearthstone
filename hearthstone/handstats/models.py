from django.db import models
from django.template import loader, Context
		
class Card(models.Model):
	name = models.CharField(max_length = 200)
	cost = models.IntegerField()
	
	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()
		
	# Generates the HTML-representation of a single card for the search bar.
	@property
	def html_search(self):
		card_template = loader.get_template('card_search_template.html')
		context = Context({'card':self})
		to_render = card_template.render(context).replace('\n','')
		return to_render
		
class RealCard(models.Model):
	nb_copy = models.IntegerField()
	prob_in_hand = models.FloatField(default=0.0)
	card = models.ForeignKey(Card)
	
	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()
		
	# Generates the HTML-representation of a real card when creating a deck.
	@property
	def html(self):
		real_card_template = loader.get_template('real_card_template_creation.html')
		context = Context({'real_card':self})
		to_render = real_card_template.render(context).replace('\n','')
		return to_render
	

class Deck(models.Model):
	name = models.CharField(max_length = 200)
	hero = models.CharField(max_length = 200)
	cards = models.ManyToManyField(RealCard)

	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()
		
	@property
	def get_cards(self):
		return self.cards.order_by('card__cost')
		
	@property
	def html_selectable(self):
		deck_template = loader.get_template('deck_selectable_template.html')
		context = Context({'deck':self})
		to_render = deck_template.render(context).replace('\n','')
		return to_render
		
	@property
	def html(self):
		deck_template = loader.get_template('deck_template.html')
		context = Context({'deck':self})
		to_render = deck_template.render(context).replace('\n','')
		return to_render
		
class DeckInGame(models.Model):
	deck = models.ForeignKey(Deck)
	cards = models.ManyToManyField(RealCard)
	
	def nb_remaining_cards(self):
		counter = 0
		for card in self.cards.all():
			counter += card.nb_copy
		return counter
	
	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()
		
		
class DeckCreation(models.Model):
	hero = models.CharField(max_length = 200)
	nb_cards = models.IntegerField()
	real_cards = models.ManyToManyField(RealCard)

	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()
		
class Game(models.Model):
	opponent_hero = models.CharField(max_length = 200)
	first_to_play = models.BooleanField()
	turn = models.IntegerField(default = 1)
	opponent_hand_cards_nb = models.IntegerField()
	opponent_remaining_cards = models.IntegerField()
	use_opponent_card_todo_list = models.ManyToManyField(Card, related_name="use_opponent_card_todo_list")
	update_opponent_prob_maybe_todo_list = models.ManyToManyField(Card, related_name="update_opponent_prob_maybe_todo_list")
	update_opponent_prob_sure_todo_list = models.ManyToManyField(Card, related_name="update_opponent_prob_sure_todo_list")
	decks = models.ManyToManyField(DeckInGame)
	
	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()
		
	@property
	def get_decks(self):
		to_return = []
		for deck_in_game in self.decks.all():
			to_return.append(deck_in_game.deck)
		return to_return

