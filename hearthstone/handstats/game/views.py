from django.shortcuts import render, redirect, get_object_or_404

def initiate_game(request):
	context = {}
	return render(request, 'initiate_game.html', context)