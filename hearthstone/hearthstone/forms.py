from django import forms
from django.forms import extras

# model to store various informations about the
# user and that are not present inside the one in
# auth.
from django.contrib.auth.models import User

class CreateNewGame(forms.Form):
	hero = forms.CharField()
	button = forms.CharField()

	def clean(self):
		cleaned_data = super(PostAnswerForm, self).clean()
		return cleaned_data
		
	def clean_hero(self):
		hero = self.cleaned_data.get('hero')
		if hero != "mage" and hero != "paladin" and hero != "hunter" and hero != "shaman" and hero != "priest" and hero != "warlock" and hero != "warrior" and hero != "druid" and hero != "rogue":
			raise forms.ValidationError("Not a valid hero.")
		else:
			return hero
			
	def clean_button(self):
		button = self.cleaned_data.get('button')
		if button != 'button-me' and button != 'button-opponent':
			raise forms.ValidationError("Not a valid button.")
		else:
			return button