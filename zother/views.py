from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from zother.forms import RegistrationForm





def main_page(request):
    return render_to_response(
            'main_page.html',
            RequestContext(request)
            )



def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            return HttpResponseRedirect('/register/success')
    else:
        form = RegistrationForm()
    variables = RequestContext(request,
        { 'form':form }
    )
    return render_to_response(
        'registration/register.html',
        variables,
        RequestContext(request)
    )
