from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from handstats.models import *

def add_card_to_deck_creation(request):
	context = {}

	if 'deck_creation_id' in request.POST and not request.POST['deck_creation_id'] == '' and 'new_card_id' in request.POST and not request.POST['new_card_id'] == '':
		deck_creation_id = request.POST['deck_creation_id']
		new_card_id = request.POST['new_card_id']

		deck_creation = get_object_or_404(DeckCreation, pk=deck_creation_id)
		card = get_object_or_404(Card, pk=new_card_id)
		
		if deck_creation.nb_cards < 30:
			already_in = False
			if deck_creation.nb_cards > 0:
				for real_card in deck_creation.real_cards.all():
					if real_card.card == card:
						already_in = True
						# Mean already at least one
						if real_card.nb_copy <= 1:
							real_card.nb_copy = real_card.nb_copy + 1
							real_card.save()
							deck_creation.nb_cards = deck_creation.nb_cards + 1
							deck_creation.save()
			
			if not already_in:
				new_real_card = RealCard(card=card, nb_copy=1)
				new_real_card.save()
				deck_creation.real_cards.add(new_real_card)
				deck_creation.nb_cards = deck_creation.nb_cards + 1
				deck_creation.save()
		
		context['deck_creation'] = deck_creation

		return render(request, 'deck_creation.json', context, content_type='application/json')

	return HttpResponse("")
	
def remove_card_from_deck_creation(request):
	context = {}

	if 'deck_creation_id' in request.POST and not request.POST['deck_creation_id'] == '' and 'card_id' in request.POST and not request.POST['card_id'] == '':
		deck_creation_id = request.POST['deck_creation_id']
		real_card_id = request.POST['card_id']
		
		deck_creation = get_object_or_404(DeckCreation, pk=deck_creation_id)
		real_card_to_delete = get_object_or_404(RealCard, pk=real_card_id)
		
		need_to_erase = True
		
		if deck_creation.nb_cards > 0:
			for real_card in deck_creation.real_cards.all():
				if real_card == real_card_to_delete:
					# Mean already at least one
					if real_card.nb_copy > 1:
						need_to_erase = False
						real_card.nb_copy = real_card.nb_copy - 1
						real_card.save()
						deck_creation.nb_cards = deck_creation.nb_cards - 1
						deck_creation.save()
		
		if need_to_erase:
			for real_card in deck_creation.real_cards.all():
				if real_card == real_card_to_delete:
					deck_creation.real_cards.remove(real_card)
					deck_creation.nb_cards = deck_creation.nb_cards - 1
					deck_creation.save()
					break
			
		context['deck_creation'] = deck_creation
		
		# If no more cards, send nothing
		if deck_creation.nb_cards < 1:
			return HttpResponse("")

		return render(request, 'deck_creation.json', context, content_type='application/json')

	return HttpResponse("")
	
def create_new_deck_creation(request):
	if 'hero' in request.POST and not request.POST['hero'] == '':
		hero = request.POST['hero']

		new_deck_creation = DeckCreation(hero=hero, nb_cards=0)
		new_deck_creation.save()

		return HttpResponse(new_deck_creation.pk)

	raise Http404
	
def submit_deck_creation(request):
	if 'deck_creation_id' in request.POST and not request.POST['deck_creation_id'] == '' and 'deck_name' in request.POST and not request.POST['deck_name'] == '':

		deck_creation_id = request.POST['deck_creation_id']
		deck_name = request.POST['deck_name']

		deck_creation = get_object_or_404(DeckCreation, pk=deck_creation_id)

		new_deck = Deck(hero=deck_creation.hero, name=deck_name)
		new_deck.save()

		for real_card in deck_creation.real_cards.all():
			new_deck.cards.add(real_card)
			
		new_deck.save()
		
		return HttpResponse("Success")
		
	return HttpResponse("")
		
		
		
		
		
		
		
	