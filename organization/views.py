from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models.base import ModelBase
from django.http import HttpResponse, Http404, HttpResponseRedirect
from vanilla import ListView, CreateView, DetailView, UpdateView
from organization.models import *
from organization.forms import *
from exams.models import ExamRecipe
import json


class ChapterList(ListView):
    model = Chapter
    context_object_name = 'chapters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_question_links'] = True
        return context


class CourseDetails(DetailView):
    model = Course
    fields = '__all__'
    context_object_name = 'course'

class EditCourseDetails(UpdateView):
    model = Course
    fields = '__all__'
    context_object_name = 'course'

class CreateCourse(CreateView):
    model = Course
    fields = '__all__'
    form_class = CourseInfoForm

    def post(self, request):
        course = Course(instructor=request.user)
        form = CourseInfoForm(request.POST, instance=course)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse('CourseDetails', kwargs={'pk': self.object.id})


@login_required
def course_list(request):
    variables = RequestContext(request, {
        'active_courses' : request.user.course_set.filter(is_active=True),
        'inactive_courses' : request.user.course_set.filter(is_active=False),
    })
    return render_to_response('organization/course_list.html', variables)


class CreateBook(CreateView):
    model= Book
    fields = '__all__'
    template_name = 'organization/create_book.html'
    
    def get_success_url(self):
        return reverse('EditBook', kwargs={'pk': self.object.id})


class BookDetails(DetailView):
    model = Book
    fields = '__all__'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_display'] = 'simple_preview'
        return context


class EditBook(BookDetails):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_book'] = True
        return context


class BookWithQuestions(BookDetails):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_question_links'] = True
        context['edit_questions'] = True
        return context


class EditBookWithQuestions(BookWithQuestions):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_book'] = True
        return context


class BookList(ListView):
    model = Book
    fields = '__all__'


@login_required
def add_chapter(request, book_id):
    """
    On GET, returns the form to be used to add a chapter.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            panel_url   : if form.is_valid, the new panel for the accordion,
            place       : if form.is_valid, the place to stick the new panel,
            form_html   : if form not valid, the html to represent the form
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'book' : book,
            'form' : form,
            'form_title' : form_title,
            'action_url' : reverse('add_chapter', kwargs={'book_id':book.id})
        })
        return render_to_response('organization/book_form.html',variables)
    
    book = get_object_or_404(Book, id=book_id)
    form_title = "Add chapter to book “{}”".format(book.name)

    if request.POST:
        chapter = Chapter(book=book, order=book.chapter_set.count())
        form = ChapterForm(request.POST,instance=chapter)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'place' : '#accordion-main',
                'action' : 'add',
                'panel_html' : get_accordion_panel(request, item=chapter),
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(ChapterForm())

@login_required
def edit_chapter(request, chapter_id):
    """
    On GET, returns the form to be used to edit the chapter.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            form_html   : if form not valid, the html to represent the form
            action      : "edit"
            label       : the id of the panel label
            name        : the new name of the section
            
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'form' : form,
            'form_title' : 'Edit Chapter',
            'item_type' : 'chapter',
            'item_id' : chapter_id,
            'action_url' : reverse('edit_chapter', kwargs={'chapter_id':chapter.id}),
        })
        return render_to_response('organization/book_form.html',variables)
    
    chapter = get_object_or_404(Chapter, id=chapter_id)

    if request.POST:
        form = ChapterForm(request.POST,instance=chapter)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'action' : 'edit',
                'label' : '#label-chapter-{}'.format(chapter.id),
                'name' : chapter.name
                
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(ChapterForm(instance=chapter))

@login_required
def edit_chapter_old(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    if request.POST:
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    else: # request.GET
        form = ChapterForm(instance=chapter)
    variables = RequestContext(request, 
        {
            'form' : form,
            'form_title' : 'Edit Chapter',
            'item_type' : 'chapter',
            'item_id' : chapter_id,
            'action_url' : reverse('edit_chapter', kwargs={'chapter_id':chapter.id}),
        })
    return render_to_response('organization/book_form.html',variables)

@login_required
def delete_item(request, item_type, item_id):
    
    if not 'confirmed' in request.GET:
        raise Http404
    Item = {
        'chapter' : Chapter,
        'section' : Section,
        'objective' : Objective,
        'question' : Question,
        'examrecipe' : ExamRecipe,
    }[item_type]
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return HttpResponse('deleted')

@login_required
def add_section(request, chapter_id):
    """
    On GET, returns the form to be used to add a section.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            panel_url   : if form.is_valid, the new panel for the accordion,
            place       : if form.is_valid, the place to stick the new panel,
            form_html   : if form not valid, the html to represent the form
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'book' : chapter.book,
            'chapter' : chapter,
            'form' : form,
            'form_title' : form_title,
            'action_url' : reverse('add_section', kwargs={'chapter_id':chapter.id})
        })
        return render_to_response('organization/book_form.html',variables)
    
    chapter = get_object_or_404(Chapter, id=chapter_id)
    form_title = "Add section to chapter “{}”".format(chapter.name)

    if request.POST:
        section = Section(chapter=chapter, order=chapter.section_set.count())
        form = SectionForm(request.POST,instance=section)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'place' : '#accordion-chapter-{}'.format(chapter.id),
                'action' : 'add',
                'panel_html' : get_accordion_panel(request, item=section),
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(ChapterForm())

@login_required
def edit_section(request, section_id):
    """
    On GET, returns the form to be used to edit the section.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            form_html   : if form not valid, the html to represent the form
            action      : "edit"
            label       : the id of the panel label
            name        : the new name of the section
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'form' : form,
            'form_title' : 'Edit Section',
            'item_type' : 'section',
            'item_id' : section_id,
            'action_url' : reverse(
                    'edit_section', 
                    kwargs={'section_id':section.id})
        })
        return render_to_response('organization/book_form.html',variables)
    
    section = get_object_or_404(Section, id=section_id)

    if request.POST:
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'action' : 'edit',
                'label' : '#label-section-{}'.format(section.id),
                'name' : section.name,
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(SectionForm(instance=section))



@login_required
def get_accordion_panel(request, item_type='', item_id='', item=None, **kwargs):
    '''
    Returns the panel for a panel for the object of type `item_type`
    with id `item_id`.
    
    This function can accept either an actual object as `item`,
    or strings for the model name (`item_type`) and id.
    (If `item` is provided, then these will be ignored.)
    '''
    if item:
        item_type = type(item).__name__.lower()
    else:
        Item = {
            'chapter' : Chapter,
            'section' : Section,
            'objective' : Objective,
            'question' : Question,
        }[item_type]
        item = get_object_or_404(Item, id=item_id)
    
    template = "organization/accordions/{}_panel.html".format(item_type)
    variables = RequestContext(request, {
        item_type : item,
        'edit_book': kwargs.get('edit_book', True),
        'edit_questions': kwargs.get('edit_questions', True),
        'add_question_links': kwargs.get('add_question_links', True),
        'question_display': 'simple_preview',
    })
    if item_type == 'question':
        if item.objective_set.count() == 1:
            variables['objective'] = item.objective_set.first()
    return render_to_string(template, variables)

@login_required
def add_objective(request, section_id):
    """
    On GET, returns the form to be used to add an objective.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            panel_url   : if form.is_valid, the new panel for the accordion,
            place       : if form.is_valid, the place to stick the new panel,
            form_html   : if form not valid, the html to represent the form
        }
    
    """
    # TODO: refactor this so that it checks for similar objectives, 
    # and offers the user a choice to use an existing one or create a new one
    
    def form_html(form):
        form_title = "Add objective to section “{}”".format(section.name)
        variables = RequestContext(request,
        {
            'section' : section,
            'form' : form,
            'form_title' : form_title,
            'action_url' : reverse('add_objective', 
                                    kwargs={'section_id':section.id})
        })
        return render_to_response('organization/book_form.html',variables)
    
    section = get_object_or_404(Section, id=section_id)

    if request.POST:
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            form.save()
            objective = form.instance
            objective.section_set.add(section)
            response_data = {
                'success' : True,
                'place' : '#accordion-section-{}'.format(section.id),
                'action' : 'add',
                'panel_html' : get_accordion_panel(request, item=objective)
                
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
            )
    # request.GET:
    return form_html(ObjectiveForm())

@login_required
def edit_objective(request, objective_id):
    """
    On GET, returns the form to be used to edit the section.
    On POST, returns a json object:
        {   success     : whether the form was valid,
            form_html   : if form not valid, the html to represent the form
            action      : "edit"
            label       : the id of the panel label
            name        : the new name of the section
        }
    """
    
    def form_html(form):
        variables = RequestContext(request,
        {
            'form' : form,
            'form_title' : 'Edit Objective',
            'item_type' : 'objective',
            'item_id' : objective_id,
            'action_url' : reverse(
                    'edit_objective', 
                    kwargs={'objective_id':objective.id})
        })
        return render_to_response('organization/book_form.html',variables)
    
    objective = get_object_or_404(Objective, id=objective_id)

    if request.POST:
        form = ObjectiveForm(request.POST, instance=objective)
        if form.is_valid():
            form.save()
            response_data = {
                'success' : True,
                'action' : 'edit',
                'label' : '#label-objective-{}'.format(objective.id),
                'name' : objective.name,
            }
        else: # form not valid
            response_data = {
                'success' : False,
                'form_html' : form_html(form)
            }
        return HttpResponse(
                json.dumps(response_data), content_type="application/json"
        )
    # request.GET:
    return form_html(ObjectiveForm(instance=objective))

@login_required
def related_courses(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    book = course.course_type.book
    related_courses = (request.user.course_set
        .filter(course_type__book=book)
        .exclude(id=course.id)
        .order_by('-start_date')
    )
    variables = RequestContext(request, {'related_courses' : related_courses})
    return render_to_response('organization/related_courses.html', variables)

