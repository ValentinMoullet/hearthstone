from django.shortcuts import render, redirect, get_object_or_404

def help(request):
	context = {}
	return render(request, 'help.html', context)