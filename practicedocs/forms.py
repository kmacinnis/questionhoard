from django import forms


class DocumentGenreationForm(forms.Form):
    title = forms.CharField()