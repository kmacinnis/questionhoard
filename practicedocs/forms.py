from django import forms
from django.forms.models import inlineformset_factory
from practicedocs.models import DocumentRecipe, BlockRecipe


FORM_INLINE = 'form-inline'
FORM_CONTROL = 'form-control'

CLASS_INLINE = {'class':FORM_INLINE}


class DocumentGenreationForm(forms.Form):
    title = forms.CharField()

class DocRecipeNameForm(forms.ModelForm):
    class Meta:
        model = DocumentRecipe
        fields = ('title',)


class BlockRecipeInlineForm(forms.ModelForm):
    class Meta:
        model = BlockRecipe
        widgets = {
                    'order': forms.TextInput(attrs=CLASS_INLINE),
                    'num_exercises': forms.TextInput(attrs=CLASS_INLINE),
                    
                }

BlockRecipeFormSet = inlineformset_factory(
    DocumentRecipe,
    BlockRecipe,
    form = BlockRecipeInlineForm,
    extra = 0,
)
