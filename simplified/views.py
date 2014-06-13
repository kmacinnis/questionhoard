from django.shortcuts import render
# from django.views.generic import CreateView, UpdateView, FormView
from vanilla import CreateView, UpdateView, FormView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from nested_formset import nestedformset_factory


from simplified.models import *
from simplified.forms import FooForm, BarInline


class ListFoo(ListView):
    model = Foo
    template_name = 'list_foo.html'

class CreateFoo(CreateView):
    model = Foo
    template_name = 'create_foo.html'
    form_class = FooForm
    
    def get_context_data(self, **kwargs):
        context = super(CreateFoo, self).get_context_data(**kwargs)
        if self.request.POST:
            context['bar_formset'] = BarInline(self.request.POST)
        else:
            context['bar_formset'] = BarInline()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        bar_formset = context['bar_formset']
        if bar_formset.is_valid():
            self.object = form.save()
            bar_formset.instance = self.object
            bar_formset.save()
            return HttpResponseRedirect(self.object.get_absolute_url())  
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditFoo(UpdateView):
    model = Foo
    template_name = 'edit_foo.html'
    form_class = FooForm

    def get_context_data(self, **kwargs):
        context = super(EditFoo, self).get_context_data(**kwargs)
        context['bar_formset'] = BarInline(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()

        bar_formset = BarInline(self.request.POST, instance=self.object)

        if bar_formset.is_valid():
            form.save()
            bar_formset.save()
            return HttpResponseRedirect(reverse('listfoo'))  
        else:
            context['form_errors'] = bar_formset.errors
            context['bar_formset'] = bar_formset
# return render_to_response('authors_books_edits.html', {'author': a, 'authorsbooks': authorsbooks, 'formset': formset, 'form_errors': form_errors}, context_instance=RequestContext(request))
            return self.render_to_response(context)


class NestedFoo(UpdateView):
    model = Foo

    def get_template_names(self):

        return ['nested_foo.html']

    def get_form_class(self):

        return nestedformset_factory(
            Foo,
            Bar,
            Meep,
        )

    def get_success_url(self):
        return reverse('listfoo')
    
