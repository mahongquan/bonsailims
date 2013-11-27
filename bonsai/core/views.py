# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from models import UserProfile
from forms import UserProfileForm
from django.core.context_processors import csrf
def index(request):
    '''
    This is the main view. User will login through the login box on the 
    top right of page. id_username and id_password are returned. Authentication
    system is pluggable.
    '''
    c={}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['id_username']
        password = request.POST['id_password']
        user = auth.authenticate(username=username, password=password) 
        if user is not None:
            auth.login(request, user)
            try:
                profile = user.get_profile()
            except Exception, e:
                profile = UserProfile(user=user, list_per_page=25)
                profile.save()
            return HttpResponseRedirect('/project/list/1')
    return render_to_response('login.html',c)# locals())

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def set_user_profile(request):
    """sets the user profile"""
    profile = request.user.get_profile()
    form = UserProfileForm(instance=profile)
    if 'next' in request.GET:
        next = request.GET['next']
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = '/'
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Your settings are updated.")
            return HttpResponseRedirect(next)
    return render_to_response('user_profile.html', locals())
    