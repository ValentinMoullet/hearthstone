from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from handstats.models import *

def get_matching_cards(request):
	context = {}

	if 'search' in request.GET and not request.GET['search'] == '':
		search = request.GET['search']

		cards = Card.objects.filter(name__contains=search).order_by('cost')[:10]

		context['cards'] = cards

		return render(request, 'cards_search.json', context, content_type='application/json')

	return HttpResponse("")



	