from django import forms
from django.forms.models import inlineformset_factory


from simplified.models import Foo, Bar
import re
import keyword

valid_barname = re.compile(r'[A-Za-z]\w*')

class BarInlineForm(forms.ModelForm):
    class Meta:
        model = Bar
    
    def clean_barname(self):
        barname = self.cleaned_data['barname']
        if (not valid_barname.match(barname)) or (barname in keyword.kwlist):
            err_mess = '''
                Barname:
                * must start with a letter; 
                * can contain only letters, digits, and the underscore (_); 
                * cannot be a reserved python keyword;
                * and can be at most 10 characters long.'''
            raise forms.ValidationError(err_mess)
        return barname
        
        

BarInline = inlineformset_factory(
    Foo,
    Bar,
    form = BarInlineForm,
    extra = 2,
    )


class FooForm(forms.ModelForm):
    class Meta:
        model = Foo
