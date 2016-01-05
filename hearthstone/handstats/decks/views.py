from django.shortcuts import render, redirect, get_object_or_404

def existing_decks(request):
	context = {}
	return render(request, 'existing_decks.html', context)
	
def create_deck(request):
	context = {}
	return render(request, 'create_deck.html', context)