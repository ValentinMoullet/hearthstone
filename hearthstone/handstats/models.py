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

class Deck(models.Model):
	name = models.CharField(max_length = 200)
	hero = models.CharField(max_length = 200)
	cards = models.ManyToManyField(Card)

	def __unicode__(self):
		return str(self.id)
	def __str__(self):
		return self.__unicode__()

