from django.shortcuts import render, redirect, get_object_or_404
from handstats.models import *

def initiate_game(request):
	context = {}
	return render(request, 'initiate_game.html', context)
	
def new_game(request):
	context = {}
	
	# Validate info
	if 'button-me' in request.POST:
		button = request.POST['button-me']
	else:
		button = request.POST['button-opponent']
		
	form = CreateNewGame(hero=request.POST['hero'], button=button)
	if not form.is_valid:
		return render(request, 'initiate_game.html', context)
		
	# Create new game
	game = Game(opponent=form.cleaned_data['hero'], )
	
	return render(request, 'game.html', context)