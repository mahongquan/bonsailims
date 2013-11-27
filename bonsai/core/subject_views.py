from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from models import Subject, Project, Sample
import forms
import datetime
from django.core.paginator import Paginator


def add(request):
	"""Adds a subject under a subscribed project."""
	if request.method == 'POST':
		s = Subject(date_time_last_updated=datetime.datetime.now(), last_updated_by=request.user)
		form = forms.SubjectForm(request.POST, instance=s)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/subjects/list/%s/1' % form.instance.project.id)
	else:
		form = forms.SubjectForm()
	form.fields["project"].queryset = request.user.project_subscriptions.all()
	return render_to_response('subjects/add.html', locals() )

def edit(request, id):
	"""Updates a subject."""
	subject = Subject.objects.get(id=id)
	if request.method == 'POST':
		subject.date_time_last_updated = datetime.datetime.now()
		subject.last_updated_by = request.user
		form = forms.SubjectForm(request.POST, instance=subject)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/subjects/list/%s/1' % form.instance.project.id)
	else:
		form = forms.SubjectForm(instance=subject)
	form.fields["project"].queryset = request.user.project_subscriptions.all()
	return render_to_response('subjects/edit.html',locals() )


def show(request, id):
	subject = Subject.objects.get(id=id)
	samples = subject.samples.all().order_by('barcode_no')
	return render_to_response('subjects/show.html', locals())

def show_by_project(request, project_id, page_num=1):
	"""Displays all the subjects of a particular project."""
	# Bring the next 10 subjects of the project
	list_per_page = request.user.get_profile().list_per_page
	paginator = Paginator(Subject.objects.filter(project__id=project_id), list_per_page)
	page = paginator.page(page_num)
	subjects = page.object_list
	project = Project.objects.get(id=project_id)
	subject_bookmarks = request.user.subject_bookmarks.all()
	form = forms.SubjectForm()
	return render_to_response('subjects/show_by_project.html', locals())

def show_by_user(request, page_num=1):
	user = request.user
	list_per_page = user.get_profile().list_per_page
	paginator = Paginator(Subject.objects.filter(last_updated_by=user), list_per_page)
	page = paginator.page(page_num)
	subjects = page.object_list
	subject_bookmarks = user.subject_bookmarks.all()
	return render_to_response('subjects/mysubjects.html', locals())


def delete(request, id):
	"""Deletes a subject and corresponding dependencies"""
	subject = Subject.objects.get(id=id)
	user = request.user
	if request.method == 'POST':
		project_id = subject.project.id
		# delete all samples of that project
		Sample.objects.filter(subject=subject).delete()
		# delete the subject
		subject.delete()
		return HttpResponseRedirect('/subjects/list/%s/1' % project_id)
	samples = subject.samples.all().order_by('barcode_no')
	form = forms.SubjectForm(instance=subject)
	return render_to_response('subjects/delete.html',locals() )

def add_bookmark(request, subject_id):
	if request.method == 'POST':
		subject = Subject.objects.get(id=subject_id)
		subject.subscribers.add( request.user )
		return HttpResponse(request.user.id)

def remove_bookmark(request, subject_id):
	if request.method == 'POST':
		subject = Subject.objects.get(id=subject_id)
		subject.subscribers.remove( request.user )
		return HttpResponse(True)

def show_bookmarks(request, page_num=1):
	user = request.user
 	paginator = Paginator(user.subject_bookmarks.all(), 10)
	page = paginator.page(page_num)
	bookmarks = page.object_list
	return render_to_response('subjects/mysubjectbookmarks.html', locals())
