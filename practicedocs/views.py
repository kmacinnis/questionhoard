from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import View
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


import random

from practicedocs.models import *
from practicedocs.forms import *
from practicedocs.handling import *
from questions.handling import output_question
from utils.handle_latex import return_pdf, return_tex
from utils.mixins import PublicOrUsersOwnMixin
from organization.models import Chapter


        
        
class DocRecipeList(LoginRequiredMixin, ListView):
    model = DocumentRecipe

    def get_queryset(self):
        return DocumentRecipe.objects.filter(created_by=self.request.user)
    

class DocRecipeDetail(PublicOrUsersOwnMixin, DetailView):
    model = DocumentRecipe
    pubilc_field_name = 'public'
    user_field_name = 'created_by'


class DocDetail(PublicOrUsersOwnMixin, DetailView):
    model = Document
    user_field_name = 'created_by'
    pubilc_field_name = 'public'


class DocList(LoginRequiredMixin, ListView):
    model = Document
    context_object_name = 'docs'
    
    def get_queryset(self):
        return Document.objects.filter(created_by=self.request.user)


class CreateDocRecipe(CreateView):
    model = DocumentRecipe
    form_class = DocRecipeNameForm
    template_name = 'practicedocs/create_docrecipe.html'

    def post(self, request):
        recipe = DocumentRecipe(created_by=request.user)
        form = DocRecipeNameForm(request.POST, instance=recipe)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


def view_document(request, document_id, filetype):
    
    def mergeable(a,b):
        return ((a.prompt == b.prompt) and (a.num_columns == b.num_columns)
                and (a.space_after == b.space_after))
    
    doc = get_object_or_404(Document, id=document_id)
    task_sets = []
    ts = TaskSet()
    for block in doc.block_set.order_by('order'):
        if not mergeable(block,ts):
            ts = TaskSet()
            ts.prompt = block.prompt
            ts.num_columns = block.num_columns
            ts.space_after = block.space_after
            task_sets.append(ts)
        for exercise in block.exercises.all():
            ts.tasks.append(
                    output_question(exercise.question, exercise.vardict))
    variables = {'doc':doc, 'task_sets':task_sets,}
    if filetype == "pdf":
        return return_pdf(request, 
            "practicedocs/doc.tex", variables, filename="latex_test.pdf")
    elif filetype == "tex":
        return return_tex(request, 
            "practicedocs/doc.tex", variables, filename="latex_test.tex")
    else:
        raise Http404


class EditDocRecipe(UpdateView):
    model = DocumentRecipe
    template_name = 'practicedocs/edit_docrecipe.html'
    form_class = DocRecipeNameForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blockrecipe_formset'] = BlockRecipeFormSet(
                                                instance=self.object)
        context['chapters'] = Chapter.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        
        blockrecipe_formset = BlockRecipeFormSet(
                self.request.POST, instance=self.object)
        if blockrecipe_formset.is_valid():
            form.save()
            blockrecipe_formset.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context['form'] = form
            context['blockrecipe_formset'] = blockrecipe_formset
            return self.render_to_response(context)


def ajax_add_blockrecipe(request):
    question_id = request.GET['question_id']
    question = get_object_or_404(Question,id=question_id)
    docrecipe_id = request.GET['docrecipe_id']
    document = get_object_or_404(DocumentRecipe,id=docrecipe_id)
    form_num = request.GET['form_num']
    new_block = BlockRecipe(question=question, document=document)
    form = BlockRecipeFormSet().empty_form
    form.instance = new_block
    form.prefix = 'blockrecipe_set-{}'.format(form_num)
    form.initial = {
        'question' : question_id,
        'document' : docrecipe_id,
    }
    variables = RequestContext(request, {'form' : form, 'form_num':form_num})
    return render_to_response('practicedocs/blockrecipe_element.html',variables)




@login_required
def generate_document(request, recipe_id):
    document_recipe = get_object_or_404(DocumentRecipe, id=recipe_id)
    if request.POST:
        form = DocumentGenreationForm(request.POST)
        if form.is_valid():
            doc = Document(
                title = form.cleaned_data['title'],
                recipe = document_recipe,
                created_by = request.user
            )
            doc.save()
            for block_recipe in document_recipe.blockrecipe_set.order_by('order'):
                question = block_recipe.question
                block = Block(
                    document = doc,
                    order = block_recipe.order,
                    recipe = block_recipe,
                    prompt = question.prompt,
                )
                block.save()
                vardicts = random.sample(
                    question.validation.vardicts, 
                    block_recipe.num_exercises
                )
                for vardict in vardicts:
                    block.exercises.get_or_create(
                        question=question, 
                        vardict=vardict
                    )
            variables = RequestContext(request, {'doc':doc})
            return HttpResponseRedirect("/practicedocs/")
    else: #request.GET
        form = DocumentGenreationForm(initial={'title':document_recipe.title})
        variables = RequestContext(request,
        {
            'form' : form,
            'document_recipe' : document_recipe,
        })
        return render_to_response('practicedocs/generate_document.html',variables)
        
        
        




