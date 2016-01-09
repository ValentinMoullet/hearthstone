from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404

from handstats.models import *

def existing_decks(request):
	context = {}
	
	if 'hero' in request.GET and request.GET['hero'] != '':
		decks = Deck.objects.filter(hero=request.GET['hero'])
		context['decks'] = decks
		context['selectable'] = True
		return render(request, 'decks.json', context, content_type='application/json')
	else:
		decks = Deck.objects.order_by('hero')
		context['decks'] = decks
		context['selectable'] = False
		return render(request, 'existing_decks.html', context)
	
	
def create_deck(request):
	context = {}
	return render(request, 'create_deck.html', context)
	
def get_deck_list(request, deck_id):
	deck = get_object_or_404(Deck, id=deck_id)
	
	context = {}
	context['deck'] = deck
	
	return render(request, 'deck_list.html', context)
	
	