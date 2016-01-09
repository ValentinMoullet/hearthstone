from django import forms
from django.forms import extras

# model to store various informations about the
# user and that are not present inside the one in
# auth.
from django.contrib.auth.models import User

class CreateNewGame(forms.Form):
	hero = forms.CharField(max_length=200)
	decks = forms.CharField(max_length=200)
	button = forms.CharField(max_length=200)

	def clean(self):
		cleaned_data = super(CreateNewGame, self).clean()
		return cleaned_data
		
	def clean_hero(self):
		hero = self.cleaned_data.get('hero')
		if hero != "mage" and hero != "paladin" and hero != "hunter" and hero != "shaman" and hero != "priest" and hero != "warlock" and hero != "warrior" and hero != "druid" and hero != "rogue":
			raise forms.ValidationError("Not a valid hero.")
		return hero
			
	def clean_decks(self):
		decks = self.cleaned_data.get('decks')
		if decks == "":
			raise forms.ValidationError("You must select at least one deck.")
		for deck_id in decks.split(","):
			if not deck_id.isdigit():
				raise forms.ValidationError("There is a problem with the ids of your decks.")
		return decks
			
	def clean_button(self):
		button = self.cleaned_data.get('button')
		if button != 'Me' and button != 'My opponent':
			raise forms.ValidationError("Not a valid button.")
		return button
			
class NextTurn(forms.Form):
	game = forms.IntegerField()
	button = forms.CharField(max_length = 200)
	
	def clean(self):
		cleaned_data = super(NextTurn, self).clean()
		return cleaned_data
			
	def clean_button(self):
		button = self.cleaned_data.get('button')
		if button != 'End turn' and button != 'End game':
			raise forms.ValidationError("Not a valid button.")
		return button