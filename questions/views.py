from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, FormView
# from vanilla import CreateView, UpdateView, FormView
import json


from questions.models import *
from questions.forms import *
from questions.handling import validate_question, preview_question
from organization.models import Objective
from organization.views import get_accordion_panel

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
    is_validated = q.is_validated
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
def create_question(request,**kwargs):
    
    def form_html(form ):
        myvars = RequestContext(request,
        {
            'form' : form,
            'randvar_formset' : randvar_formset,
            'condition_formset' : condition_formset,
            'answerchoices_formset' : answerchoices_formset,
            'action' : 'Create',
            'objective' : objective,
            'for_obj' : for_obj,
            'action_url' : reverse(
                'create_question_for_objective', kwargs={'obj_id':objective_id})
        })
        return render_to_response('questions/question_form.html',myvars)

    objective_id = kwargs.get('obj_id','')
    if objective_id:
        objective = get_object_or_404(Objective, id=objective_id)
        for_obj = 'for Objective "{}"'.format(objective.name)
    else:
        objective, for_obj = '',''

    if request.POST:
        response_data = {}
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
                if objective:
                    question.objective_set.add(objective)
                response_data = {
                    'success' : True,
                    'panel_html' : get_accordion_panel(
                            request, 'question', question.id
                    ),
                    'place' : '#accordion-objective-{}'.format(objective.id),
                    'action' : 'add', 
                }
        if not response_data:
            response_data = {
                'success' : False,
                'form_html' : form_html(form),
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    else: #request.GET
        form = QuestionEntryForm()
        randvar_formset = RandVarsInline(instance=Question())
        condition_formset = ConditionsInline(instance=Question())
        answerchoices_formset = AnswerChoicesInline(instance=Question())
        return form_html(form)


class CreateQuestion(CreateView):
    model = Question
    template_name = 'questions/create_question.html'
    form_class = QuestionEntryForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objective_id = self.kwargs.get('obj_id')
        if objective_id:
            context['objective'] = Objective.objects.get(id=objective_id)
        
        context['action'] = 'Create'
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
        self.object = form.save(commit=False)
        context = self.get_context_data()
        
        randvar_formset = RandVarsInline(self.request.POST, instance=self.object)
        condition_formset = ConditionsInline(self.request.POST, instance=self.object)
        answerchoices_formset = AnswerChoicesInline(self.request.POST, instance=self.object)

        all_formsets = [randvar_formset, condition_formset, answerchoices_formset]
        if all([f.is_valid() for f in all_formsets]):
            # lg.debug('good formsets')
            self.object.save()
            randvar_formset.save()
            condition_formset.save()
            answerchoices_formset.save()
            # check to see if we're assigning an objective to this question:
            if 'objective' in context:
                self.object.objective_set.add(context['objective'])

            return HttpResponseRedirect(self.object.get_absolute_url())  
        else: # there's a problem with one of the formsets
            context['form'] = form
            context['randvar_formset'] = randvar_formset
            context['condition_formset'] = condition_formset
            context['answerchoices_formset'] = answerchoices_formset
            return self.render_to_response(context)

    def post(self, request, **kwargs):
        self.object = None
        question = Question(created_by=request.user)
        form = QuestionEntryForm(request.POST, instance=question)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form) 


class EditQuestionBase(UpdateView):
    model = Question
    template_name = 'questions/edit_question.html'
    form_class = QuestionEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
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
            form.save()
            randvar_formset.save()
            condition_formset.save()
            answerchoices_formset.save()
            # check to see if we're attempting to validate this question:
            if 'is_validated' in context:
                return HttpResponseRedirect(
                    reverse('validate', kwargs={'pk': self.object.id}))

            return HttpResponseRedirect(self.object.get_absolute_url())  
        else: # there's a problem with one of the formsets
            context['form'] = form
            context['randvar_formset'] = randvar_formset
            context['condition_formset'] = condition_formset
            context['answerchoices_formset'] = answerchoices_formset
            return self.render_to_response(context)

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'success' : True,
                'id' : self.object.pk,
                'name' : self.object.name,
                'panel_html' : get_accordion_panel(
                        request, self.object, self.object.pk
                ),
            }
            return self.render_to_json_response(data)
        else:
            return response


class EditQuestion(AjaxableResponseMixin, EditQuestionBase):
    pass


class ValidateQuestion(EditQuestion):
    template_name = 'questions/validation.html'

    def get_context_data(self, **kwargs):
        context = super(ValidateQuestion, self).get_context_data(**kwargs)
        is_validated = self.object.is_validated
        if not is_validated:
            context['validation_errors'] = validate_question(
                                            self.object, self.request.user)
            if context['validation_errors'] is None:
                is_validated = True
        context['is_validated'] = is_validated
        
        return context

@login_required
def validate(request, question_id):
    ajax = 'ajax' in request.GET
    if not ajax:
        return ValidateQuestion.as_view()(request, pk=question_id)
    question = get_object_or_404(Question, id=question_id)
    if question.is_validated:
        return HttpResponse('validated')
    validation_errors = validate_question(question, request.user)
    if validation_errors is None:
        return HttpResponse('validated')
    error_html = render_to_string('questions/validation_errors.html', 
            {'validation_errors' : validation_errors}
    )
    response_data = {
        'error_html' : error_html,
        'form_url' : reverse('EditQuestion', kwargs={'pk':question_id}),
    }
    return HttpResponse(
                json.dumps(response_data), content_type="application/json"
    )


