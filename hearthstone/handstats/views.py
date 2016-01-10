from django.shortcuts import render, redirect, get_object_or_404

def index(request):
	context = {}
	print("IN")
	print(request)
	return render(request, 'index.html', context)