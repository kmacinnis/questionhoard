from django import forms
from django.forms.models import inlineformset_factory
from questions.models import Question, RandVar, Condition, AnswerChoice
import re
import keyword

valid_varname = re.compile(r'[A-Za-z]\w*')




class RandVarsInlineForm(forms.ModelForm):
    class Meta:
        model = RandVar
        fields = '__all__'
    
    def run_validators(self):
        return
    
    def clean_varname(self):
        # TODO: Figure out why this doesn't work.  
        # In the meantime, we will check for errors when validating the question.

        vname = self.cleaned_data['varname']
        if not valid_varname.match(vname):
            err_mess = '''
                Random Variable names must start with a letter and 
                can contain only letters, digits, and underscores
                '''
            raise forms.ValidationError(err_mess)
        if vname in keyword.kwlist:
            err_mess = 'Random Variable names cannot be a reserved python keyword'
            raise forms.ValidationError(err_mess)
            
        return vname
        
        

RandVarsInline = inlineformset_factory(
    Question,
    RandVar,
    form = RandVarsInlineForm,
    extra = 1,
    )
RandVarsInline.description = "Random Variable"

ConditionsInline = inlineformset_factory(
    Question,
    Condition,
    fields = '__all__',
    extra = 1,
    )
ConditionsInline.description = "Condtion"

AnswerChoicesInline = inlineformset_factory(
    Question,
    AnswerChoice,
    fields = '__all__',
    extra = 1,
    )
AnswerChoicesInline.description = "AnswerChoice"




class QuestionEntryForm(forms.ModelForm):
    
    class Meta:
        model = Question
        exclude = ('created_by',)
        
        # TODO: add hidden widgets for fields that don't show up in html form
        # comment, packages, look for others
