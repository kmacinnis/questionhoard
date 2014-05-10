from django.shortcuts import get_object_or_404, render_to_response
from vanilla import ListView, DetailView, CreateView
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404


import random

from practicedocs.models import *
from practicedocs.forms import *
from practicedocs.handling import *
from questions.handling import output_question
from zother.handle_latex import return_pdf, return_tex

# Create your views here.

class DocRecipeList(ListView):
    model = DocumentRecipe


class DocRecipeDetail(DetailView):
    model = DocumentRecipe


class DocList(ListView):
    model = Document
    context_object_name = 'docs'


class CreateDocRecipe(CreateView):
    model = DocumentRecipe
    form_class = DocRecipeCreateForm
    template_name = 'practicedocs/create_docrecipe.html'

    def post(self, request):
        recipe = DocumentRecipe(created_by=request.user)
        form = DocRecipeCreateForm(request.POST, instance=recipe)
        if form.is_valid():
            return self.form_valid(form)


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
            ts.tasks.append(output_question(exercise.question, exercise.vardict))
    variables = {'doc':doc, 'task_sets':task_sets,}
    if filetype == "pdf":
        return return_pdf(request, 
            "practicedocs/doc.tex", variables, filename="latex_test.pdf")
    elif filetype == "tex":
        return return_tex(request, 
            "practicedocs/doc.tex", variables, filename="latex_test.tex")
    else:
        raise Http404


class EditRecipe(UpdateView):
    model = DocumentRecipe
    


def edit_recipe(request, recipe_id):
    topics = Topic.objects.all()
    recipe = get_object_or_404(DocumentRecipe, id=recipe_id)
    form = 0





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
                    question.validated.vardicts, 
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
        
        
        




