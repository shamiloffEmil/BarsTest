from django import forms
from django.forms import ModelChoiceField

from .models import Recruit, TestHandShadow, Result, Answer, Sith

class RecruitForm(forms.ModelForm):
	class Meta:
		model = Recruit
		fields = ('name', 'planetOfResidence', 'age', 'email')

class TestHandShadowForm(forms.ModelForm):
	class Meta:
		model = TestHandShadow
		fields = ('orderСode', 'question')

class ResultForm(forms.ModelForm):
	class Meta:
		model = Result
		fields = ('recruit', 'test', 'answer')

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ('answer',)

class SithForm(forms.ModelForm):
	sith = ModelChoiceField(Sith.objects.all(), empty_label=None)

	class Meta:
		model = Sith
		fields = ()
