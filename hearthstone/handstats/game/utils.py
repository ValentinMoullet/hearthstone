from handstats.models import *
from handstats.forms import *

import math

def nCr(n,r):
    f = math.factorial
    return float(f(n) / f(r) / f(n-r))

'''
def prob_having_in_hand(nb_copies, nb_remaining_cards_in_deck, nb_cards_in_hand):
	to_return = 1.0
	for i in range(nb_remaining_cards_in_deck, nb_remaining_cards_in_deck - nb_cards_in_hand, -1):
		to_return *= (i - nb_copies) / float(i)
	return 1.0 - to_return
'''

def prob_having_in_starting_hand(nb_copies, nb_remaining_cards_in_deck, nb_cards_in_hand):
	return 1.0 - nCr(nb_remaining_cards_in_deck - nb_copies, nb_cards_in_hand) / nCr(nb_remaining_cards_in_deck, nb_cards_in_hand)
	
	
def use_opponent_card_action(game, card):
	# Remove real card(s) from deck(s)
	to_remove = 0
	for deck in game.decks.all():
		for real_card in deck.cards.all():
			if real_card.card == card:
				to_remove += 1
				if real_card.nb_copy == 1:
					game.decks.remove(real_card)
				elif real_card.nb_copy == 2:
					real_card.nb_copy -= 1
					# Divide by 2 prob for the remaining one (not sure about that)
					real_card.prob_in_hand /= 2
				real_card.save()
				break
				
	# Update prob for all cards
	already_updated = []
	for deck in game.decks.all():
		for real_card in deck.cards.all():
			if real_card.card == card:
				# Probability of having card in hand knowing that it was not the other one (P(InHand|1 is not))
				real_card.prob = (real_card.prob_in_hand * (game.opponent_hand_cards_nb - 1) / game.opponent_hand_cards_nb) / (real_card.prob_in_hand * (game.opponent_hand_cards_nb - 1) / game.opponent_hand_cards_nb + (1 - real_card.prob_in_hand) * 1)
				real_card.save()
	
	game.opponent_hand_cards_nb -= 1
	game.opponent_remaining_cards -= to_remove
	game.save()
	
def update_opponent_prob_maybe_action(game, card):
	for deck in game.decks.all():
		for real_card in deck.cards.all():
			if real_card.card == card:
				to_remove += 1
				if real_card.nb_copy == 1:
					game.decks.remove(real_card)
				elif real_card.nb_copy > 1:
					real_card.nb_copy -= 1
				break
				
	'''
	TO COMPLETE
	'''
	
	game.opponent_remaining_cards -= to_remove
	game.save()
	
def update_opponent_prob_sure_action(game, card):
	for deck in game.decks.all():
		for real_card in deck.cards.all():
			if real_card.card == card:
				to_remove += 1
				if real_card.nb_copy == 1:
					game.decks.remove(real_card)
				elif real_card.nb_copy > 1:
					real_card.nb_copy -= 1
				break
				
	'''
	TO COMPLETE
	'''
	
	game.opponent_remaining_cards -= to_remove
	game.save()