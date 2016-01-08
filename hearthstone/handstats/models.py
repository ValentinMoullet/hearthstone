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
	def html(self):
		deck_template = loader.get_template('deck_template.html')
		context = Context({'deck':self})
		to_render = deck_template.render(context).replace('\n','')
		return to_render
		
class DeckCreation(models.Model):
	hero = models.CharField(max_length = 200)
	nb_cards = models.IntegerField()
	real_cards = models.ManyToManyField(RealCard)

	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()

