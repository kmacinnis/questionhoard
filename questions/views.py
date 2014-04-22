from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# from django.views.generic import CreateView, UpdateView, FormView
from vanilla import CreateView, UpdateView, FormView


from questions.models import *
from questions.forms import *
from questions.handling import validate_question, preview_question

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
lg = logging.getLogger('lg')

def index(request):
    question_list = Question.objects.all()
    # output = ', '.join([q.question_name for q in question_list])
    # return HttpResponse(output)
    # template = loader.get_template('questions/index.html')
    context = {'question_list': question_list}
    return render(request, 'questions/index.html', context)

def mathjaxtest(request):
    question_list = Question.objects.all()
    # output = ', '.join([q.question_name for q in question_list])
    # return HttpResponse(output)
    # template = loader.get_template('questions/index.html')
    context = {'question_list': question_list}
    return render(request, 'questions/mathjaxtest.html', context)


@login_required
def detail(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    randvar_formset = RandVarsInline(instance=q)
    randvar_formset.extra = 0
    condition_formset = ConditionsInline(instance=q)
    condition_formset.extra = 0
    answerchoices_formset = AnswerChoicesInline(instance=q)
    answerchoices_formset.extra = 0
    try:
        is_validated = (q.validated.last_verified >= q.last_updated)
    except ObjectDoesNotExist:
        is_validated = False
    variables = RequestContext(request,
        {
            'question' : q,
            'randvar_dataset' : randvar_formset,
            'condition_dataset' : condition_formset,
            'answerchoices_dataset' : answerchoices_formset,
            'is_validated' : is_validated,
        }
        
    )
    return render_to_response('questions/detail_page.html', variables)


def preview(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    variables = preview_question(q)
    variables['question'] = q
    variables = RequestContext(request,variables)
    return render_to_response('questions/question_preview.html', variables)
    






@login_required
def create_question(request):
    if request.POST:
        question = Question(created_by=request.user)
        form = QuestionEntryForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            randvar_formset = RandVarsInline(request.POST, instance=question)
            condition_formset = ConditionsInline(request.POST, instance=question)
            answerchoices_formset = AnswerChoicesInline(request.POST, instance=question)
            all_formsets = [randvar_formset, condition_formset, answerchoices_formset]
            
            if all([f.is_valid() for f in all_formsets]):
                question.save()
                randvar_formset.save()
                condition_formset.save()
                answerchoices_formset.save()
                return HttpResponseRedirect(
                    "/questions/{}".format(question.id))
    else: #request.GET
        form = QuestionEntryForm()
        randvar_formset = RandVarsInline(instance=Question())
        condition_formset = ConditionsInline(instance=Question())
        answerchoices_formset = AnswerChoicesInline(instance=Question())
    variables = RequestContext(request,
    {
        'form' : form,
        'randvar_formset' : randvar_formset,
        'condition_formset' : condition_formset,
        'answerchoices_formset' : answerchoices_formset,
    })
    return render_to_response('questions/create_question.html',variables)


class CreateQuestion(CreateView):
    model = Question
    template_name = 'questions/create_question.html'
    form_class = QuestionEntryForm
    
    def get_context_data(self, **kwargs):
        context = super(CreateQuestion, self).get_context_data(**kwargs)
        if self.request.POST:
            context['randvar_formset'] = RandVarsInline(self.request.POST)
            context['condition_formset'] = ConditionsInline(self.request.POST)
            context['answerchoices_formset'] = AnswerChoicesInline(self.request.POST)
        else:
            context['randvar_formset'] = RandVarsInline()
            context['condition_formset'] = ConditionsInline()
            context['answerchoices_formset'] = AnswerChoicesInline()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        randvar_formset = context['randvar_formset']
        if randvar_formset.is_valid():
            self.object = form.save()
            randvar_formset.instance = self.object
            randvar_formset.save()
            return HttpResponseRedirect(self.object.get_absolute_url())  
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def post(self, request):
        question = Question(created_by=request.user)
        form = QuestionEntryForm(request.POST, instance=question)
        if form.is_valid():
            return self.form_valid(form)



class EditQuestion(UpdateView):
    model = Question
    template_name = 'questions/edit_question.html'
    form_class = QuestionEntryForm

    def get_context_data(self, **kwargs):
        context = super(EditQuestion, self).get_context_data(**kwargs)
        context['randvar_formset'] = RandVarsInline(instance=self.object)
        context['condition_formset'] = ConditionsInline(instance=self.object)
        context['answerchoices_formset'] = AnswerChoicesInline(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()

        randvar_formset = RandVarsInline(self.request.POST, instance=self.object)
        condition_formset = ConditionsInline(self.request.POST, instance=self.object)
        answerchoices_formset = AnswerChoicesInline(self.request.POST, instance=self.object)

        all_formsets = [randvar_formset, condition_formset, answerchoices_formset]
        if all([f.is_valid() for f in all_formsets]):
            # lg.debug('good formsets')
            form.save()
            randvar_formset.save()
            condition_formset.save()
            answerchoices_formset.save()
            # check to see if we're attempting to validate this question:
            if 'is_validated' in context:
                return HttpResponseRedirect(
                    reverse('validate', kwargs={'pk': self.object.id}))

            return HttpResponseRedirect(self.object.get_absolute_url())  
        else:
            context['form'] = form
            context['randvar_formset'] = randvar_formset
            context['condition_formset'] = condition_formset
            context['answerchoices_formset'] = answerchoices_formset
            return self.render_to_response(context)


class ValidateQuestion(EditQuestion):
    template_name = 'questions/validation.html'

    def get_context_data(self, **kwargs):
        context = super(ValidateQuestion, self).get_context_data(**kwargs)
        q = self.object
        try:
            is_validated = (q.validated.last_verified > q.last_updated)
        except ObjectDoesNotExist:
            is_validated = False
        if not is_validated:
            context['validation_errors'] = validate_question(
                                            self.object, self.request.user)
            if context['validation_errors'] == None:
                is_validated = True
        context['is_validated'] = is_validated
        context['called_from'] = 2
        
        return context




