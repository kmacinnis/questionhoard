from django import forms
from django.forms.models import inlineformset_factory
from practicedocs.models import DocumentRecipe, BlockRecipe


class DocumentGenreationForm(forms.Form):
    title = forms.CharField()

class DocRecipeNameForm(forms.ModelForm):
    class Meta:
        model = DocumentRecipe
        fields = ('title',)

BlockRecipeFormSet = inlineformset_factory(
    DocumentRecipe,
    BlockRecipe,
    extra = 0,
)
