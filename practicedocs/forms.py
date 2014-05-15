from django import forms
from django.forms.models import inlineformset_factory
from practicedocs.models import DocumentRecipe, BlockRecipe


FORM_INLINE = 'form-inline'
FORM_CONTROL = 'form-control'
INPUT_SIZE = 'input-sm'

CLASS_INLINE = {'class':FORM_INLINE}
CLASS_CONTROL = {'class':' '.join((FORM_CONTROL,INPUT_SIZE))}


class DocumentGenreationForm(forms.Form):
    title = forms.CharField()

class DocRecipeNameForm(forms.ModelForm):
    class Meta:
        model = DocumentRecipe
        fields = ('title',)


class BlockRecipeInlineForm(forms.ModelForm):
    class Meta:
        model = BlockRecipe
        fields = [
            'num_columns',
            'num_exercises',
            'order',
            'space_after',
            'question',
            ]
        widgets = {
            'question':forms.HiddenInput(),
            'order': forms.TextInput(attrs=CLASS_CONTROL),
            'num_exercises': forms.TextInput(attrs=CLASS_CONTROL),
            'num_columns': forms.TextInput(attrs=CLASS_CONTROL),
            'space_after': forms.TextInput(attrs=CLASS_CONTROL),
            'ORDER': forms.TextInput(attrs=CLASS_CONTROL),
        }


BlockRecipeFormSet = inlineformset_factory(
    DocumentRecipe,
    BlockRecipe,
    form = BlockRecipeInlineForm,
    extra = 0,
    can_order = True,
)
BlockRecipeFormSet.description = 'Block of questions'