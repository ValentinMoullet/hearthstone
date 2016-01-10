from django.shortcuts import render, redirect, get_object_or_404
from handstats.models import *
from handstats.forms import *
from handstats.game.utils import *

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.views.decorators.csrf import csrf_exempt

def initiate_game(request):
	context = {}
	return render(request, 'initiate_game.html', context)
	
@csrf_exempt
def new_game(request):
	context = {}
	
	form = CreateNewGame(request.POST)

	if not form.is_valid():
		return render(request, 'initiate_game.html', context)
	
	# Retrieve all selected decks
	deck_ids = request.POST['decks']
	deck_ids_list = []
	for deck_id in deck_ids.split(","):
		deck_ids_list.append(int(deck_id))
		
	decks = Deck.objects.filter(id__in=deck_ids_list)
		
	# Create new game
	first_to_play = form.cleaned_data['button'] == 'Me'
	if first_to_play:
		# Add coin?
		opponent_hand_cards_nb = 5
	else:
		opponent_hand_cards_nb = 4

	opponent_remaining_cards = decks.count() * 30
	game = Game(opponent_hero=form.cleaned_data['hero'], first_to_play=first_to_play, opponent_hand_cards_nb=opponent_hand_cards_nb, opponent_remaining_cards=opponent_remaining_cards)
	game.save()
	
	# Creating new DeckInGame with copy of RealCard and initiate probs
	for deck in decks:
		deck_in_game = DeckInGame(deck=deck)
		deck_in_game.save()
		for real_card in deck.cards.all():
			real_card_copy = RealCard(nb_copy=real_card.nb_copy, prob_in_hand=prob_having_in_starting_hand(real_card.nb_copy, game.opponent_remaining_cards, game.opponent_hand_cards_nb), card=real_card.card)
			real_card_copy.save()
			deck_in_game.cards.add(real_card_copy)
		deck_in_game.save()
		game.decks.add(deck_in_game)
	game.save()
	
	context['game'] = game
	context['decks'] = Deck.objects.filter(hero=game.opponent_hero)
	
	return render(request, 'game.html', context)
	
# All actions are done whe ending the turn
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
	
	# Update with new decks (1st thing to do)
	all_selected_decks = Deck.objects.filter(id__in=deck_ids)
	decks_to_check = game.decks.all()
	for deck in all_selected_decks.all():
		# If checked a new deck
		if not deck in decks_to_check:
			new_deck_in_game = DeckInGame(deck=deck)
			new_deck_in_game.save()
			for real_card in deck.cards.all():
				real_card_copy = RealCard(nb_copy=real_card.nb_copy, prob_in_hand=prob_having_in_starting_hand(real_card.nb_copy, game.opponent_remaining_cards, game.opponent_hand_cards_nb), card=real_card.card)
				real_card_copy.save()
				new_deck_in_game.cards.add(real_card_copy)
			new_deck_in_game.save()
			game.decks.add(new_deck_in_game)
			game.opponent_remaining_cards += new_deck_in_game.nb_remaining_cards()
		else:
			decks_to_check.remove(deck)
			
	# If some decks are still in decks_to_check, it means they have been un-checked, so we have to remove them from game
	for deck_to_remove in decks_to_check:
		game.opponent_remaining_cards -= deck_to_remove.nb_remaining_cards()
		game.decks.remove(deck_to_remove)
		
	game.save()
	
	# Execute all actions that have been done during last turn (2nd thing to do)
	for card in game.use_opponent_card_todo_list.all():
		use_opponent_card_action(game, card)
		game.use_opponent_card_todo_list.remove(card)
	for card in game.update_opponent_prob_maybe_todo_list.all():
		update_opponent_prob_maybe_action(game, card)
		game.update_opponent_prob_maybe_todo_list.remove(card)
	for card in game.update_opponent_prob_sure_todo_list.all():
		game.update_opponent_prob_sure_todo_list.remove(card)
		update_opponent_prob_sure_action(game, card)
	
	
	# Here means next turn
	
	# Update prob when drawing 1 card
	for deck in game.decks.all():
		for real_card in deck.cards.all():
			real_card.prob_in_hand += (1 - real_card.prob_in_hand) * (float(real_card.nb_copy) / (game.opponent_remaining_cards - game.opponent_hand_cards_nb))
			real_card.save()
	game.turn += 1
	game.opponent_hand_cards_nb += 1
	game.save()
	
	context['game'] = game
	context['decks'] = Deck.objects.filter(hero=game.opponent_hero)
	
	return render(request, 'game.html', context)
	
def use_opponent_card(request):
	context = {}
	
	if 'game_id' in request.POST and request.POST['game_id'] != '' and 'card_id' in request.POST and request.POST['card_id'] != '':
		game = get_object_or_404(Game, id=request.POST['game_id'])
		card = get_object_or_404(Card, id=request.POST['card_id'])
		
		game.use_opponent_card_todo_list.add(card)
		
		return HttpResponse("Success")
		
	return HttpResponse("Failure")
	
def update_opponent_prob_maybe(request):
	context = {}
	
	if 'game_id' in request.POST and request.POST['game_id'] != '' and 'card_id' in request.POST and request.POST['card_id'] != '':
		game = get_object_or_404(Game, id=request.POST['game_id'])
		card = get_object_or_404(Card, id=request.POST['card_id'])
		
		game.update_opponent_prob_maybe_todo_list.add(card)
		
		return HttpResponse("Success")
		
	return HttpResponse("Failure")
	
def update_opponent_prob_sure(request):
	context = {}
	
	if 'game_id' in request.POST and request.POST['game_id'] != '' and 'card_id' in request.POST and request.POST['card_id'] != '':
		game = get_object_or_404(Game, id=request.POST['game_id'])
		card = get_object_or_404(Card, id=request.POST['card_id'])
		
		game.update_opponent_prob_sure_todo_list.add(card)
		
		return HttpResponse("Success")
		
	return HttpResponse("Failure")
		
		