from django import forms
# from .models import Book

class SearchForm(forms.Form):
    by_title = forms.CharField(label='Search book title', max_length=400, help_text='e.g: python java flex')
    by_year = forms.CharField(required=False, label='Filter by years (comma separated)', max_length=400, help_text='e.g: 1998, 2010, 2002')
    by_author = forms.CharField(required=False, label='Filter by authors (comma separated)', max_length=400, help_text='e.g: Ted Neward, John Hazzaz')
    by_category = forms.CharField(required=False, label='Filter by categories (comma separated)', max_length=400, help_text='e.g: Internet, Java')

class MakePaymentForm(forms.Form):
    CHOICES = [('credit','Credit'), ('debit','Debit')]
    card_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'radio_1'}))
    # radio = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'radio_1'}))
    amount = forms.FloatField(label='Amount', min_value=0.1)
