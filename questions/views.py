from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# from django.views.generic import CreateView, UpdateView, FormView
from vanilla import CreateView, UpdateView, FormView, ListView
import json

from copy import deepcopy


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
    context = {'question_list': question_list}
    return render(request, 'questions/index.html', context)


class QuestionList(ListView):
    model = Question


@login_required
def detail(request, question_id):
    # TODO: Redo this, so that it doesn't have to rely on the formsets to display.
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


class QuestionBase(object):
    just_form = 'questions/question_form.html'
    model = Question
    form_class = QuestionEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = self.get_action_url(**kwargs)
        context['randvar_formset'] = RandVarsInline(instance=self.object)
        context['condition_formset'] = ConditionsInline(instance=self.object)
        context['answerchoices_formset'] = AnswerChoicesInline(instance=self.object)
        return context

    def get_posted(self, request):
        self.object = self.get_object()
        form = self.get_form(data=request.POST, instance=self.object)
        randvar_formset = RandVarsInline(self.request.POST, instance=self.object)
        condition_formset = ConditionsInline(self.request.POST, instance=self.object)
        answerchoices_formset = AnswerChoicesInline(self.request.POST, instance=self.object)
        formsets = {
            'randvar_formset' : randvar_formset,
            'condition_formset' : condition_formset,
            'answerchoices_formset' : answerchoices_formset
        }
        if form.is_valid() and all([f.is_valid() for f in formsets.values()]):
            return self.form_valid_contextuple(form, formsets)
        return self.form_invalid_contextuple(form, formsets)

    def form_valid_contextuple(self, form, formsets):
        context = self.get_context_data()
        form.save()
        for formset in formsets.values():
            formset.save()
        return (True, context)

    def form_invalid_contextuple(self, form, formsets):
        context = self.get_context_data()
        context['form'] = form
        context.update(formsets)
        return (False, context)

    def get_response_data(self, context):
        response_data = {
            'action' : self.action,
            'form_html' : render_to_string(self.just_form, 
                    RequestContext(self.request,context)
            ),            
        }
        if self.object.id:
            response_data.update({
                'validated' : self.object.is_validated,
                'panel_html':get_accordion_panel(self.request,item=self.object),
            })
        return response_data


class CreateQuestionBase(QuestionBase, CreateView):
    template_name = 'questions/create_question.html'
    model = Question
    form_class = QuestionEntryForm
    
    def get_action_url(self, **kwargs):
        return reverse('CreateQuestion', kwargs=self.kwargs)
    
    def get_object(self, **kwargs):
        return Question(created_by=self.request.user)
    
    def get_response_data(self, context):
        response_data = super().get_response_data(context)
        if 'obj_id' in self.kwargs:
            obj_id = self.kwargs['obj_id']
            response_data['place'] = '#accordion-objective-{}'.format(obj_id)
        return response_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        context['action_url'] = self.get_action_url(**kwargs)
        context['randvar_formset'] = RandVarsInline()
        context['condition_formset'] = ConditionsInline()
        context['answerchoices_formset'] = AnswerChoicesInline()
        if 'obj_id' in self.kwargs:
            objective = get_object_or_404(Objective, id=self.kwargs['obj_id'])
            context['objective'] = objective
        return context

    def form_valid_contextuple(self, form, formsets):
        contextuple = super().form_valid_contextuple(form, formsets)        
        if 'obj_id' in self.kwargs:
            objective = get_object_or_404(Objective, id=self.kwargs['obj_id'])
            self.object.objective_set.add(objective)
        return contextuple


class EditQuestionBase(QuestionBase, UpdateView):
    model = Question
    template_name = 'questions/edit_question.html'
    just_form = 'questions/question_form.html'
    form_class = QuestionEntryForm

    def get_action_url(self, **kwargs):
        return reverse('EditQuestion', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['randvar_formset'] = RandVarsInline(instance=self.object)
        context['condition_formset'] = ConditionsInline(instance=self.object)
        context['answerchoices_formset'] = AnswerChoicesInline(instance=self.object)
        return context

    def get_posted(self, request):
        self.object = self.get_object()
        form = self.get_form(data=request.POST, instance=self.object)
        randvar_formset = RandVarsInline(self.request.POST, instance=self.object)
        condition_formset = ConditionsInline(self.request.POST, instance=self.object)
        answerchoices_formset = AnswerChoicesInline(self.request.POST, instance=self.object)
        formsets = {
            'randvar_formset' : randvar_formset,
            'condition_formset' : condition_formset,
            'answerchoices_formset' : answerchoices_formset
        }
        if form.is_valid() and all([f.is_valid() for f in formsets.values()]):
            return self.form_valid_contextuple(form, formsets)
        return self.form_invalid_contextuple(form, formsets)


class AjaxyMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get(self, request, *args, **kwargs):
        ajax = ('ajax' in self.request.GET) or request.is_ajax()
        self.object = self.get_object()
        if not ajax:
            return super().get(request, *args, **kwargs)
        form = self.get_form(instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_json_response(self.get_response_data(context))

    def post(self, request, *args, **kwargs):
        success, context = self.get_posted(request)
        ajax = ('ajax' in self.request.GET) or request.is_ajax()
        if not ajax:
            if success:
                return HttpResponseRedirect(self.object.get_absolute_url())
            return self.render_to_response(context)
        # Ajax request
        response_data = super().get_response_data(context)
        response_data['success'] = success
        return self.render_to_json_response(response_data)


class CreateQuestion(AjaxyMixin, CreateQuestionBase):
    action = 'add'


class EditQuestion(AjaxyMixin, EditQuestionBase):
    action = 'edit question'


class ValidateQuestion(AjaxyMixin, EditQuestionBase):
    template_name = 'questions/validation.html'
    action = 'validate question'

    def get_action_url(self, **kwargs):
        return reverse('ValidateQuestion', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_validated = self.object.is_validated
        if not is_validated:
            context['validation_errors'] = validate_question(
                                            self.object, self.request.user)
            if context['validation_errors'] is None:
                is_validated = True
        context['is_validated'] = is_validated
        return context

    def get_response_data(self, context):
        response_data = super().get_response_data(context)
        response_data['error_html'] = render_to_string(
                'questions/validation_errors.html', context
        )
        return response_data


class DuplicateQuestion(CreateQuestion):

    def get_action_url(self, **kwargs):
        return reverse('CreateQuestion', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        orig_id = self.kwargs['orig_id']
        orig = get_object_or_404(Question, id=orig_id)
        
        if 'obj_id' in kwargs:
            objective = get_object_or_404(Objective, id=obj_id)
        else:
            objective = None
        
        RandVarsInlineDup = inlineformset_factory(
            Question,
            RandVar,
            extra = orig.randvar_set.count(),
            )
        RandVarsInlineDup.description = "Random Variable"
        randvar_formset = RandVarsInlineDup(instance=Question())
        
        ConditionsInlineDup = inlineformset_factory(
            Question,
            Condition,
            extra = orig.condition_set.count(),
            )
        ConditionsInlineDup.description = "Condtion"
        condition_formset = ConditionsInlineDup(instance=Question())

        AnswerChoicesInlineDup = inlineformset_factory(
            Question,
            AnswerChoice,
            extra = orig.answerchoice_set.count(),
            )
        AnswerChoicesInlineDup.description = "AnswerChoice"
        answerchoices_formset = AnswerChoicesInlineDup
        
        dup = get_object_or_404(Question, id=orig_id)
        dup.pk = None
        dup.name += ' (copy)'
        if dup.comment:
            dup.comment += '\n'
        dup.comment += 'Duplicated from question {}'.format(orig_id)
        form = QuestionEntryForm(instance=dup)
        
        context = RequestContext(self.request, {
            'form' : form,
            'randvar_formset' : randvar_formset,
            'condition_formset' : condition_formset,
            'answerchoices_formset' : answerchoices_formset,
            'action' : 'Duplicate',
            'action_url' : self.get_action_url(**kwargs),
            'objective' : get
        })
        return context

    def get_response_data(self, context):
        orig_id = self.kwargs['orig_id']
        orig = get_object_or_404(Question, id=orig_id)
        
        response_data = super().get_response_data(context)

        objects_and_attributes = [
            ('randvar_set', orig.randvar_set.all(), ('varname','varposs')),
            ('condition_set', orig.condition_set.all(), ('condition_text', )),
            ('answerchoice_set', orig.answerchoice_set.all(), 
                ('choice_text', 'choice_expr', 'choice_type', 'pin', 'comment'))
        ]

        initial_data = []
        
        for set_name, obj_list, attributes in objects_and_attributes:
            for i, obj in enumerate(obj_list):
                for attr in attributes:
                    initial_data.append({
                        'id' : '#id_{}-{}-{}'.format(set_name, i, attr),
                        'value' : obj.__getattribute__(attr)
                    })
                
        
        response_data['formset_data'] = initial_data
        return response_data
        
        # for i, randvar in enumerate(orig.randvar_set.all()):
        #     for attr in ('varname', 'varposs'):
        #     initial_data.append({
        #         'id' : '#id_randvar_set-{}-varposs'.format(i),
        #         'value'
        #
        #     })
        #     randvar_data['randvar_set-%s-varposs' % i] = randvar.varposs
        #
        # count = orig.randvar_set.count()
        # randvar_data = {
        #     'randvar_set-TOTAL_FORMS' : count,
        #     'randvar_set-INITIAL_FORMS' : count,
        # }
        # randvar_formset = RandVarsInline(randvar_data, initial=randvar_initial)
        
        # cond_initial = [
        #     {'condition_text' : cond.condition_text}
        #     for cond in orig.condition_set.all()
        # ]
        # count = orig.condition_set.count()
        # cond_data = {
        #     'condition_set-TOTAL_FORMS' : count,
        #     'ondition_set-INITIAL_FORMS' : count
        # }
        # for i, cond in enumerate(orig.condition_set.all()):
        #     cond_data['condition_set-%s-condition_text'%i] = cond.condition_text
        # cond_data['condition_set-TOTAL_FORMS'] = i+1
        # cond_data['condition_set-INITIAL_FORMS'] = i+1
        #
        # ans_data = {}
        # for i, ans in enumerate(orig.answerchoice_set.all()):
        #     ans_data['answerchoice_set-%s-choice_text' % i] = ans.choice_text
        #     ans_data['answerchoice_set-%s-choice_expr' % i] = ans.choice_expr
        #     ans_data['answerchoice_set-%s-choice_type' % i] = ans.choice_type
        #     ans_data['answerchoice_set-%s-pin' % i] = ans.pin
        #     ans_data['answerchoice_set-%s-comment' % i] = ans.comment
        # ans_data['answerchoice_set-TOTAL_FORMS'] = i+1
        # ans_data['answerchoice_set-INITIAL_FORMS'] = i+1
        #
        #
        # # randvar_formset = RandVarsInline(randvar_data, initial=randvar_initial)
        # # randvar_formset.data = randvar_data
        # condition_formset = ConditionsInline()
        # condition_formset.data = cond_data
        # answerchoices_formset = AnswerChoicesInline()
        # answerchoices_formset.data = ans_data
        #      
        
        
        