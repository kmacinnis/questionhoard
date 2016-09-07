from django.shortcuts import get_object_or_404, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import transaction
from django.db.models import Max
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView


from copy import deepcopy
from collections import Counter
import random
import json

from exams.models import *
from exams.forms import *
from exams.handling import get_form_number, create_answer_choices
from organization.models import Chapter
from questions.handling import output_question
from utils.handle_latex import return_pdf, return_tex


class ExamRecipeList(ListView):
    model = ExamRecipe


@login_required
def examrecipe_list(request):
    variables = RequestContext(request, {
        'examrecipe_set' : request.user.examrecipe_set.all(),
    })
    return render_to_response('exams/examrecipe_list.html', variables)
    


class ExamRecipeDetail(DetailView):
    model = ExamRecipe
    context_object_name = 'exam_recipe'


class PartRecipeDetail(DetailView):
    model = ExamPartRecipe
    context_object_name = 'part'


class CreateExamRecipe(CreateView):
    model = ExamRecipe
    form_class = ExamRecipeForm
    template_name = 'exams/create_recipe.html'
    
    def get_form(self):
        form = ExamRecipeForm()
        course_id = self.kwargs.get('course_id')
        if course_id:
            form.fields['course'].widget = forms.HiddenInput()
            form.fields['course'].initial = course_id
        return form

    def post(self, request, *args, **kwargs):
        recipe = ExamRecipe(created_by=request.user)
        form = ExamRecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class CreateExamPartRecipe(CreateView):
    model = ExamPartRecipe
    form_class = PartRecipeForm

    def get_success_url(self):
        return reverse('EditPartRecipe', kwargs={'pk': self.object.id})

    def post(self, request, **kwargs):
        exam_id = self.kwargs.get('exam_id')
        exam = get_object_or_404(ExamRecipe, id=exam_id)
        agg = exam.exampartrecipe_set.aggregate(Max('order'))
        try:
            order = agg['order__max']
        except TypeError:
            order = 1
        part = ExamPartRecipe(exam=exam, order=0)
        form = PartRecipeForm(request.POST, instance=part)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class EditExamRecipe(UpdateView):
    model = ExamRecipe
    template_name = 'exams/edit_exam.html'
    form_class = ExamRecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditPartRecipe(UpdateView):
    model = ExamPartRecipe
    template_name = 'exams/edit_part.html'
    form_class = PartRecipeForm
    
    def get_context_data(self, **kwargs):
        ep = self.object
        context = super().get_context_data(**kwargs)
        context['question_formset'] = QuestionInlineFormSet(instance=ep)
        context['book'] = ep.exam.book
        context['edit_book'] = False
        return context
        
    def form_valid(self, form):
        context = self.get_context_data()
        
        question_formset = QuestionInlineFormSet(
                self.request.POST, instance=self.object)
        if question_formset.is_valid():
            form.save()
            question_formset.save()
            return HttpResponseRedirect(self.object.exam.get_absolute_url())
        else:
            context['form'] = form
            context['question_formset'] = question_formset
            return self.render_to_response(context)


class UpdatePartRecipe(UpdateView):
    '''This will replace EditPartRecipe, and will not use formsets at all.'''
    model = ExamPartRecipe
    template_name = 'exams/update_part.html'
    context_object_name = 'part'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.object.exam.book
        context['edit_book'] = False
        return context
    


@login_required
def ajax_add_examrecipequestion(request):
    question_id = request.GET['question_id']
    partrecipe_id = request.GET['partrecipe_id']
    form_num = request.GET['form_num']
    style = request.GET['style']
    question = get_object_or_404(Question,id=question_id)
    exam_part = get_object_or_404(ExamPartRecipe,id=partrecipe_id)
    new_question = ExamRecipeQuestion(question=question, part=exam_part)
    
    form = QuestionInlineFormSet().empty_form
    form.instance = new_question
    form.prefix = 'examrecipequestion_set-{}'.format(form_num)
    form.initial = {
        'question' : question_id,
        'part' : partrecipe_id,
        'name' : question.name,
        'order' : int(form_num) + 1,
    }
    if style in BASIC_QUESTION_TYPES:
        form.initial['question_style'] = style
    variables = RequestContext(request, {'form' : form, 'form_num':form_num})
    return render_to_response('exams/question_element.html',variables)


@login_required
@transaction.atomic
def generate_exam(request, recipe_id):
    
    def append_question(question, item, part, question_counter):
        vardict = question.random_vardict()
        text = output_question(
                question, vardict, set_choice_position=False)['questiontext']
        new_question = ExamQuestion(
            question = question,
            vardict = vardict,
            part = part,
            item = item,
            question_text = text,
            order = question_counter,
            space_after = item.space_after,
        )
        new_question.save()

    exam_recipe = get_object_or_404(ExamRecipe,id=recipe_id)
    generated_set = GeneratedSet(
        recipe = exam_recipe,
        course = exam_recipe.course,
        created_by = request.user,
    )
    generated_set.save()
    for i in range(exam_recipe.number_of_forms):
        exam = Exam(
            generated_set = generated_set,
            title = exam_recipe.display_title,
            form = get_form_number(exam_recipe.form_number_style, i),
        )
        exam.save()
        question_counter = 0
        for part_recipe in exam_recipe.exampartrecipe_set.all():
            
            part = ExamPart(
                exam = exam,
                title = part_recipe.title,
                show_title = part_recipe.show_title,
                instructions = part_recipe.instructions,
                order = part_recipe.order,
                question_style = part_recipe.question_style,
            )
            part.save()
            for item in part_recipe.examrecipeitem_set.select_subclasses():
                if isinstance(item,ExamRecipeQuestion):
                    question_counter += 1
                    append_question(item.question, item, part, question_counter)
                elif isinstance(item,ExamRecipePool):
                    if item.questions.count() < item.choose:
                        continue
                    question_list = random.sample(
                            list(item.questions.all()), item.choose
                    )
                    for q in question_list:
                        question_counter += 1
                        append_question(q, item, part, question_counter)
                else:
                    raise ValueError("ExamRecipeItem should only be subclassed as ExamRecipeQuestion or ExamRecipePool")
            if part_recipe.question_style == 'mc':
                create_answer_choices(
                        part.examquestion_set.all(), 
                        max_choices=exam_recipe.max_number_choices
                )
            elif part.question_style == 'mix':
                create_answer_choices(
                        part.examquestion_set.filter(item__question_style='mc'),
                        max_choices=exam_recipe.max_number_choices
                )
            if part_recipe.shuffled:
                randlist = list(part.examquestion_set.all())
                random.shuffle(randlist)
                for i, q in enumerate(randlist):
                    q.order = i
                    q.save()
    exam_recipe.frozen = True
    exam_recipe.save()
    return HttpResponseRedirect(exam_recipe.get_absolute_url())  


@login_required
def view_exam(request, exam_id, filetype):
    exam = get_object_or_404(Exam, id=exam_id)
    variables = {'exam' : exam, 'user':request.user}
    if filetype == "pdf":
        return return_pdf(request, 
            "exams/exam.tex", variables, filename="latex_test.pdf")
    elif filetype == "tex":
        return return_tex(request, 
            "exams/exam.tex", variables, filename="latex_test.tex")
    else:
        raise Http404


@login_required
def unfreeze_exam_recipe(request, exam_recipe_id=None, action=None):
    exam_recipe = get_object_or_404(ExamRecipe, id=exam_recipe_id)
    if not (request.user == exam_recipe.created_by or request.user.is_superuser):
        raise Http404
    if action == 'keep':
        for exam_set in exam_recipe.generatedset_set.all():
            comment = 'Created from previous version of {}.'.format(
                    exam_recipe.private_title)
            try:
                exam_set.comment += ' | ' + comment
            except TypeError:
                exam_set.comment = comment
            exam_set.save()
        exam_recipe.generatedset_set.clear()
    elif action == 'delete':
        for g in exam_recipe.generatedset_set.all():
            g.delete()
    else:
        raise Http404
    exam_recipe.frozen = False
    exam_recipe.save()
    return HttpResponseRedirect(exam_recipe.get_absolute_url())  

@login_required
@transaction.atomic
def duplicate_exam_recipe(request, recipe_id):
    exam_recipe = get_object_or_404(ExamRecipe, id=recipe_id)
    recipe_copy = deepcopy(exam_recipe)
    recipe_copy.id = None
    recipe_copy.frozen = False
    recipe_copy.private_title += ' (copy)'
    if request.user != recipe_copy.created_by:
        recipe_copy.created_by = request.user
    recipe_copy.save()
    for part in exam_recipe.exampartrecipe_set.all():
        part_copy = deepcopy(part)
        part_copy.id = None
        part_copy.exam = recipe_copy
        part_copy.save()
        all_items = part.examrecipeitem_set.select_subclasses()
        questions = [i for i in all_items if type(i)==ExamRecipeQuestion]
        pools = [i for i in all_items if type(i)==ExamRecipePool]
        for q in questions:
            q_copy = ExamRecipeQuestion(
                part = part_copy,
                order = q.order,
                name = q.name,
                question_style = q.question_style,
                space_after = q.space_after,
                question = q.question,
            )
            q_copy.save()
        for p in pools:
            p_copy = ExamRecipePool(
                part = part_copy,
                order = p.order,
                name = p.name,
                question_style = p.question_style,
                space_after = p.space_after,
                choose = p.choose,
            )
            p_copy.save()
            for q in p.questions.all():
                p_copy.questions.add(q)
    return HttpResponseRedirect(recipe_copy.get_absolute_url())


class AddPool(generic.edit.CreateView):
    model = ExamRecipePool
    template_name = 'exams/create_pool.html'
    form_class = PoolForm
    
    def get_initial(self):
        part_recipe_id = self.kwargs.get('part_recipe_id')
        part = get_object_or_404(ExamPartRecipe, id=part_recipe_id)
        order = part.examrecipeitem_set.count() + 1
        return {'part': part, 'order': order, 'choose': 1}

    def get_success_url(self):
        return reverse('EditPool', kwargs={'pk': self.object.id})


class EditPool(UpdateView):
    model = ExamRecipePool
    template_name = 'exams/pool_question_list.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = Chapter.objects.all()
        context['book'] = self.object.exam().book()
        return context

    def get_success_url(self):
        return reverse('EditPartRecipe', kwargs={'pk': self.object.part.id})


def ajax_add_question_to_pool(request):
    question_id = request.GET['question_id']
    pool_id = request.GET['pool_id']
    question = get_object_or_404(Question,id=question_id)
    pool = get_object_or_404(ExamRecipePool,id=pool_id)
    pool.questions.add(question)
    pool.save()
    
    variables = RequestContext(request, {'question':question})
    return render_to_response('exams/pool_question.html',variables)


def ajax_remove_question_from_pool(request):
    question_id = request.GET['question_id']
    pool_id = request.GET['pool_id']
    question = get_object_or_404(Question,id=question_id)
    pool = get_object_or_404(ExamRecipePool,id=pool_id)
    pool.questions.remove(question)
    return HttpResponse('success')


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)

def add_question_to_exam(request):
    '''Ajax function'''
    question_id = request.GET['question_id']
    exampart_id = request.GET['exampart_id']
    question = get_object_or_404(Question,id=question_id)
    exampart = get_object_or_404(ExamPartRecipe, id=exampart_id)
    exam_owner = exampart.exam.created_by
    if (request.user == exam_owner) or request.user.is_superuser:
        new_q = ExamRecipeQuestion(
            question = question,
            part = exampart,
            order = request.GET['order'],
            question_style = request.GET['question_style'],
            space_after = request.GET['space_after'],
        )
        new_q.save()
        response_data = {
            'success' : True,
            'item_div' : render_to_string('exams/item.html', {'item': new_q})
        }
    else:
        response_data = {
            'success': False,
            'err_mess': 'You do not have permission to add items to this exam.'
        }
    return render_to_json_response(response_data)

def remove_item_from_exam(request):
    item_id = request.GET['item_id']
    item = get_object_or_404(ExamRecipeItem, id=item_id)
    item_owner = item.exam().created_by
    if (request.user == item_owner) or request.user.is_superuser:
        item.delete()
        response_data = {
            'success' : True,
        }
    else:
        response_data = {
            'success' : False,
            'err_mess' : 'You do not have permission to remove this item.',
        }
    return render_to_json_response(response_data)

def focus_pool(request):
    if request.POST:
        print(request.POST)
        exampart = get_object_or_404(ExamPartRecipe, id=request.POST['part_id'])
        pool_id = request.POST['pool_id']
        if pool_id == 'new':
            form = PoolForm(request.POST)
            pool = ExamRecipePool()
        else:
            pool = get_object_or_404(ExamRecipePool, id=pool_id)
            form = PoolForm(request.POST, instance=pool)
        if form.is_valid():
            pool = ExamRecipePool(
                name = form.cleaned_data['name'],
                choose = form.cleaned_data['choose'],
                part = exampart,
                order = form.cleaned_data['order'],
                space_after = form.cleaned_data['space_after'],
            )
            pool.save()
            question_list = request.POST['question_list'].split(',')
            pool.questions.add(*question_list)
            
            response_data = {
                'submitted' : True,
                'item_div' : render_to_string('exams/item.html', {'item': pool})
            }
            return render_to_json_response(response_data)

    else: # request.GET
        exampart_id = request.GET['exampart_id']
        exampart = get_object_or_404(ExamPartRecipe, id=exampart_id)
        pool_id = request.GET['pool_id']
    
        if pool_id == 'new':
            pool = ExamRecipePool(name='New Pool', choose=1, part=exampart)
            if exampart.question_style != 'mix':
                pool.question_style = exampart.question_style
            question_list = []
        else:
            pool = get_object_or_404(ExamRecipePool, id=pool_id)
            question_list = pool.questions.all()
        form = PoolForm(instance=pool)
    variables = RequestContext(request, {
        'pool' : pool,
        'form' : form,
    })
    response_data = {
        'submitted' : False,
        'form' : render_to_string('exams/focus_pool.html', variables)
    }
    return render_to_json_response(response_data)

def edit_item(request, item_id):
    try:
        item = ExamRecipeItem.objects.get_subclass(id=item_id)
    except DoesNotExist:
        raise Http404
    item_type = item.type()
    # Right now, this should only be called for ExamRecipeQuestion's
    
    

    if request.POST:
        pass
    else: #request.GET
        pass
        # TODO: make a tiny form to replace the item_div.  Form only needs
        # space_after and question_style (if the exampart is 'mix')
            
            
            

@login_required
def set_preferences(request):
    if request.POST:
        prefs = FormattingPreferences.objects.get(user=request.user)
        form = PreferencesForm(request.POST,instance=prefs)
        if form.is_valid():
            prefs = form.save()
            return HttpResponse('success')
    else: # request.GET
        prefs,_ = FormattingPreferences.objects.get_or_create(user=request.user)
        form = PreferencesForm(instance=prefs)
    variables = RequestContext(request, {
        'form' : form,
    })
    return render_to_response('exams/preferences_form.html', variables)


