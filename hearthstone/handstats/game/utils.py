from handstats.models import *
from handstats.forms import *

import math

def nCr(n,r):
	if n < r:
		return 0.0
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
	if nb_copies < 1:
		return 0.0
	return 1.0 - nCr(nb_remaining_cards_in_deck - nb_copies, nb_cards_in_hand) / nCr(nb_remaining_cards_in_deck, nb_cards_in_hand)
	
def prob_having_two_in_starting_hand(nb_copies, nb_remaining_cards_in_deck, nb_cards_in_hand):
	if nb_copies < 2:
		return 0.0
	return 1.0 - (nCr(nb_remaining_cards_in_deck - nb_copies, nb_cards_in_hand) + nCr(nb_remaining_cards_in_deck - nb_copies, nb_cards_in_hand - 1)) / nCr(nb_remaining_cards_in_deck, nb_cards_in_hand)
	
	
def use_all_opponent_cards_action(game, cards):
	
	total_to_remove = 0

	for card in cards:
		# Remove real card(s) from deck(s)
		to_remove = 0 # 1 same card from all decks
		for deck in game.decks.all():
			for real_card in deck.cards.all():
				if real_card.card == card:
					to_remove += 1
					if real_card.nb_copy == 1:
						deck.cards.remove(real_card)
					elif real_card.nb_copy == 2:
						real_card.nb_copy -= 1
						# Divide by 2 prob for the remaining one (not sure about that)
						real_card.prob_in_hand = real_card.prob_two_in_hand
						real_card.prob_two_in_hand = 0.0
					real_card.save()
					break
					
		total_to_remove += to_remove
	
	for card in cards:
		'''
		# Remove card from deck abstraction
		real_card_abstraction = game.opponent_deck_abstraction.cards.get(card=card)
		real_card_abstraction.nb_copy -= to_remove
		if real_card_abstraction.nb_copy == 0:
			# If no more, remove it
			game.opponent_deck_abstraction.cards.remove(real_card_abstraction)
		else:
			# If remains some, re-compute
			real_card_abstraction.prob_in_hand = prob_having_in_starting_hand(real_card_abstraction.nb_copy, game.opponent_remaining_cards, game.opponent_hand_cards_nb)
			real_card_abstraction.save()
		'''
		
		# Update prob for all cards (is it really useful since we use deck abstraction???)
		for deck in game.decks.all():
			for real_card in deck.cards.all():
				if real_card.card == card:
					print("useless")
					# Probability of having card in hand knowing that it was not the other one (P(InHand|1 is not))
					# NOT SURE AT ALL!!!!!
					#real_card.prob_in_hand = (real_card.prob_in_hand * (game.opponent_hand_cards_nb - len(cards)) / game.opponent_hand_cards_nb) / (real_card.prob_in_hand * (game.opponent_hand_cards_nb - 1) / game.opponent_hand_cards_nb + (1 - real_card.prob_in_hand) * 1)
					#print(real_card.prob_two_in_hand)
					#real_card.prob_two_in_hand = (real_card.prob_two_in_hand * (game.opponent_hand_cards_nb - len(cards)) / game.opponent_hand_cards_nb) / (real_card.prob_two_in_hand * (game.opponent_hand_cards_nb - 1) / game.opponent_hand_cards_nb + (1 - real_card.prob_two_in_hand) * 1)
					#print(real_card.prob_two_in_hand)
					#real_card.save()
				else:
					# Probability of having card in hand knowing that it was not the other one (P(InHand|1 is not))
					# NOT SURE AT ALL!!!!!
					print(real_card.prob_in_hand)
					real_card.prob_in_hand = (real_card.get_prob_only_one_in_hand * nCr(game.opponent_hand_cards_nb - 1, len(cards)) + real_card.prob_two_in_hand * nCr(game.opponent_hand_cards_nb - 2, len(cards))) / nCr(game.opponent_hand_cards_nb, len(cards))
					print(real_card.prob_in_hand)
					real_card.prob_two_in_hand = (real_card.prob_two_in_hand * nCr(game.opponent_hand_cards_nb - 2, len(cards))) / nCr(game.opponent_hand_cards_nb, len(cards))
					real_card.save()
					
	game.opponent_hand_cards_nb -= len(cards)
	game.opponent_remaining_cards -= total_to_remove
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