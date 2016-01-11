from django.shortcuts import render, redirect, get_object_or_404
from handstats.models import *
from handstats.forms import *
from handstats.game.utils import *

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.views.decorators.csrf import csrf_exempt

NB_CARDS_IN_DECK = 30

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

	opponent_remaining_cards = decks.count() * NB_CARDS_IN_DECK
	
	# Creating new DeckInGame with copy of RealCard and initiate probs
	total_prob_for_card = {} # Map from Card to the pair (sum of all the prob_in_hand of all decks, sum of nb_copy of all deck)
	decks_in_game = []
	for deck in decks:
		deck_in_game = DeckInGame(deck=deck)
		deck_in_game.save()
		for real_card in deck.cards.all():
			real_card_copy = RealCard(nb_copy=real_card.nb_copy, prob_in_hand=prob_having_in_starting_hand(real_card.nb_copy, NB_CARDS_IN_DECK, opponent_hand_cards_nb), prob_two_in_hand=prob_having_two_in_starting_hand(real_card.nb_copy, NB_CARDS_IN_DECK, opponent_hand_cards_nb), card=real_card.card)
			real_card_copy.save()
			# Check if not already created in total prob
			if not real_card.card in total_prob_for_card:
				total_prob_for_card[real_card.card] = []
				total_prob_for_card[real_card.card].append(0.0)
				total_prob_for_card[real_card.card].append(0)
			total_prob_for_card[real_card.card][0] += real_card_copy.prob_in_hand
			total_prob_for_card[real_card.card][1] += real_card_copy.nb_copy
			deck_in_game.cards.add(real_card_copy)
		deck_in_game.save()
		decks_in_game.append(deck_in_game)
	
	# Go over total_prob_for_card and create THE abstract deck
	deck_abstraction = DeckAbstraction()
	deck_abstraction.save()
	for key, value in total_prob_for_card.iteritems():
		real_card = RealCard(nb_copy=value[1], prob_in_hand=value[0]/float(decks.count()), card=key)
		real_card.save()
		deck_abstraction.cards.add(real_card)
	deck_abstraction.save()
	
	game = Game(opponent_hero=form.cleaned_data['hero'], first_to_play=first_to_play, opponent_hand_cards_nb=opponent_hand_cards_nb, opponent_remaining_cards=opponent_remaining_cards, opponent_deck_abstraction=deck_abstraction) # opponent_deck_abstraction is bullshit
	game.save()
	for deck_in_game in decks_in_game:
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
	decks_to_check = game.get_decks
	for deck in all_selected_decks.all():
		# If checked a new deck
		if not deck in decks_to_check:
			new_deck_in_game = DeckInGame(deck=deck)
			new_deck_in_game.save()
			
			game.decks.add(new_deck_in_game)
			game.opponent_remaining_cards += new_deck_in_game.nb_remaining_cards()
			for real_card in deck.cards.all():
				# Update decks_in_game
				real_card_copy = RealCard(nb_copy=real_card.nb_copy, prob_in_hand=prob_having_in_starting_hand(real_card.nb_copy, NB_CARDS_IN_DECK - game.cards_used_by_opponent.count(), game.opponent_hand_cards_nb), prob_two_in_hand=prob_having_two_in_starting_hand(real_card.nb_copy, NB_CARDS_IN_DECK, game.opponent_hand_cards_nb), card=real_card.card)
				real_card_copy.save()
				new_deck_in_game.cards.add(real_card_copy)
				
				'''
				# Update opponent_deck_abstraction
				if real_card.card in game.opponent_deck_abstraction.get_cards():
					real_card_abstraction = game.opponent_deck_abstraction.cards.get(card=real_card.card)
					real_card_abstraction.nb_copy += real_card.nb_copy
					real_card_abstraction.prob_in_hand = prob_having_in_starting_hand(real_card_abstraction.nb_copy, game.opponent_remaining_cards, game.opponent_hand_cards_nb)
					real_card_abstraction.save()
				else:
					real_card_abstraction = RealCard(nb_copy=real_card.nb_copy, prob_in_hand=prob_having_in_starting_hand(real_card.nb_copy, game.opponent_remaining_cards, game.opponent_hand_cards_nb), card=real_card.card)
					real_card_abstraction.save()
				'''	
				
			new_deck_in_game.save()
			game.decks.add(new_deck_in_game)
		else:
			# Deck still checked
			# Remove from list because OK
			decks_to_check.remove(deck)
			
	# If some decks are still in decks_to_check, it means they have been un-checked, so we have to remove them from game
	for deck_to_remove in decks_to_check:
		deck_in_game = game.decks.get(deck=deck_to_remove)
		game.opponent_remaining_cards -= deck_in_game.nb_remaining_cards()
		game.decks.remove(deck_in_game)
		'''
		# Update deck abstraction
		for real_card in deck_in_game.cards.all():
			real_card_abstraction = game.opponent_deck_abstraction.cards.get(card=real_card.card)
			real_card_abstraction.nb_copy -= real_card.nb_copy
			if real_card_abstraction.nb_copy == 0:
				# If no more, remove it
				game.opponent_deck_abstraction.cards.remove(real_card_abstraction)
			else:
				# If remains some, re-compute
				real_card_abstraction.prob_in_hand = prob_having_in_starting_hand(real_card_abstraction.nb_copy, game.opponent_remaining_cards, game.opponent_hand_cards_nb)
				real_card_abstraction.save()
		'''
	game.save()
	
	# Execute all actions that have been done during last turn (2nd thing to do)
	use_all_opponent_cards_action(game, game.use_opponent_card_todo_list.all())
	for card in game.use_opponent_card_todo_list.all():
		game.use_opponent_card_todo_list.remove(card)
	'''
	TO COMPLETE
	for card in game.update_opponent_prob_maybe_todo_list.all():
		update_opponent_prob_maybe_action(game, card)
		game.update_opponent_prob_maybe_todo_list.remove(card)
	for card in game.update_opponent_prob_sure_todo_list.all():
		game.update_opponent_prob_sure_todo_list.remove(card)
		update_opponent_prob_sure_action(game, card)
	'''
	
	# Here means next turn
	
	# Update prob when drawing 1 card
	
	# Update all decks
	total_prob_for_card = {} # Map from Card to the sum of all the prob_in_hand of all decks
	for deck in game.decks.all():
		for real_card in deck.cards.all():
			#real_card.prob_in_hand += (1 - real_card.prob_in_hand) * (float(real_card.nb_copy) / (game.opponent_remaining_cards - game.opponent_hand_cards_nb))
			biased_prob_only_one_in_hand = real_card.get_biased_prob - real_card.get_biased_prob_for_two
			real_card.prob_in_hand = real_card.get_biased_prob + (1 - real_card.get_biased_prob) * (float(real_card.nb_copy) / (deck.nb_remaining_cards() - game.opponent_hand_cards_nb))
			real_card.prob_two_in_hand = real_card.get_biased_prob_for_two + biased_prob_only_one_in_hand * (1.0 / (deck.nb_remaining_cards() - game.opponent_hand_cards_nb))
			real_card.bias_coeff = 1.0 # Only place where we should re-initialize the coeff
			real_card.save()
			# Check if not already created in total prob
			if not real_card.card in total_prob_for_card:
				total_prob_for_card[real_card.card] = []
				total_prob_for_card[real_card.card].append(0.0)
				total_prob_for_card[real_card.card].append(0)
			total_prob_for_card[real_card.card][0] += real_card.prob_in_hand
			total_prob_for_card[real_card.card][1] += real_card.nb_copy
	
	'''
	for real_card in game.opponent_deck_abstraction.cards.all():
		real_card.prob_in_hand = real_card.get_biased_prob + (1 - real_card.get_biased_prob) * (float(real_card.nb_copy) / (game.opponent_remaining_cards - game.opponent_hand_cards_nb))
		real_card.bias_coeff = 1.0
		real_card.save()
	'''
	
	cards_to_remove = game.opponent_deck_abstraction.get_cards() # Here to check if we have to remove some cards in the deck_abstraction
	for key, value in total_prob_for_card.iteritems(): # key being Card and value being a pair: (prob, nb_copy)
		# If already in, just update it
		if key in game.opponent_deck_abstraction.get_cards():
			real_card = game.opponent_deck_abstraction.cards.get(card=key)
			real_card.prob_in_hand = value[0] / float(game.decks.count())
			real_card.nb_copy = value[1]
			real_card.save()
		# If not in, add it
		else:
			real_card = RealCard(nb_copy=value[1], prob_in_hand=value[0]/float(decks.count()), card=key)
			real_card.save()
			game.opponent_deck_abstraction.cards.add(real_card)
		cards_to_remove.remove(key)
	game.opponent_deck_abstraction.save()
	
	game.turn += 1
	game.opponent_hand_cards_nb += 1
	game.save()
	
	# Remove cards that are not here anymore
	for card in cards_to_remove:
		game.opponent_deck_abstraction.remove_card(card)
	
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
		
		