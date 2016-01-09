from django.shortcuts import render, redirect, get_object_or_404
from handstats.models import *
from handstats.forms import *

from django.views.decorators.csrf import csrf_exempt

def initiate_game(request):
	context = {}
	return render(request, 'initiate_game.html', context)
	
@csrf_exempt
def new_game(request):
	context = {}
	
	form = CreateNewGame(request.POST)
	print(form)
	print(request.POST)

	if not form.is_valid():
		return render(request, 'initiate_game.html', context)
	
	# Retrieve all selected decks
	deck_ids = request.POST['decks']
	deck_ids_list = []
	for deck_id in deck_ids.split(","):
		deck_ids_list.append(int(deck_id))
		
	decks = Deck.objects.filter(id__in=deck_ids_list)
		
	# Create new game
	game = Game(opponent_hero=form.cleaned_data['hero'], first_to_play=form.cleaned_data['button'] == 'Me')
	game.save()
	for deck in decks:
		game.decks.add(deck)
	game.save()
	
	context['game'] = game
	context['decks'] = Deck.objects.filter(hero=game.opponent_hero)
	
	return render(request, 'game.html', context)
	
def end_turn(request):
	context = {}
	
	# Get decks checked
	deck_ids = request.POST.getlist('checkbox[]')
	
	form = NextTurn(request.POST)
	if not form.is_valid() or len(deck_ids) <= 0:
		context['form_errors'] = "Invalid form"
		return render(request, 'game.html', context)
	
	game = get_object_or_404(Game, id=form.cleaned_data['game'])
	
	# See if end of game
	if form.cleaned_data['button'] == 'End game':
		game.delete()
		return render(request, 'index.html', context)
		
	# Here means next turn
	game.turn += 1
	game.opponent_cards_nb += 1
	new_decks = Deck.objects.filter(id__in=deck_ids)
	game.decks = new_decks
	game.save()
	
	context['game'] = game
	context['decks'] = Deck.objects.filter(hero=game.opponent_hero)
	
	return render(request, 'game.html', context)