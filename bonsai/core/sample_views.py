from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from models import Sample, Subject, Project
import forms
import datetime
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator
from analysis import models as analysis_models

def add(request):
	user = request.user
	if request.method == 'POST':
		s = Sample()
		s.date_time_last_updated = datetime.datetime.now()
		s.last_updated_by = request.user
		form = forms.SampleForm(request.POST, instance=s)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/samples/list/bysubject/%s/1' % form.instance.subject.id)
	else:
		form = forms.SampleForm()
	subscriptions = user.project_subscriptions.all().order_by('project_code')
	form.fields['subject'].queryset = Subject.objects.filter(project__in=subscriptions)
	return render_to_response('samples/add.html', locals() )

def edit(request, id):
	sample = Sample.objects.get(id=id)
	user = request.user
	if request.method == 'POST':
		sample.date_time_last_updated = datetime.datetime.now()
		sample.last_updated_by = request.user
		form = forms.SampleForm(request.POST, instance=sample)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/samples/list/bysubject/%s/1' % form.instance.subject.id)
	else:
		form = forms.SampleForm(instance=sample)
	subscriptions = user.project_subscriptions.all().order_by('project_code')
	form.fields['subject'].queryset = Subject.objects.filter(project__in=subscriptions)
	return render_to_response('samples/edit.html', locals())

def show(request, id):
	sample = Sample.objects.get(id=id)
	subject = sample.subject
	samples = subject.samples.all().order_by('barcode_no')
	return render_to_response('samples/show.html', locals())

def show_by_project(request, project_id, page_num=1):
	"""Displays all the samples of a given project page by page."""
	user = request.user
	subscriptions = user.project_subscriptions.all()
	project = Project.objects.get(id=project_id)
	list_per_page = user.get_profile().list_per_page
	paginator = Paginator(Sample.objects.filter(subject__project=project), list_per_page)
	page = paginator.page(page_num)
	samples = page.object_list
	sample_bookmarks = user.sample_bookmarks.all()
	return render_to_response('samples/show_by_project.html', locals())

def show_by_subject(request, subject_id, page_num=1):
	"""Displays all the samples of a given subject page by page"""
	subject = Subject.objects.get(id=subject_id)
	user = request.user
	list_per_page = user.get_profile().list_per_page
	paginator = Paginator(subject.samples.all(), list_per_page)
	page = paginator.page(page_num)
	samples = page.object_list
	sample_bookmarks = user.sample_bookmarks.all()
	return render_to_response('samples/show_by_subject.html', locals())

def show_by_user(request, page_num=1):
	user = request.user
	list_per_page = user.get_profile().list_per_page
	paginator = Paginator(Sample.objects.filter(last_updated_by=user), list_per_page)
	page = paginator.page(page_num)
	samples = page.object_list
	sample_bookmarks = user.sample_bookmarks.all()
	return render_to_response('samples/mysamples.html', locals())

def search(request):
	if request.method=='POST':
		kw = request.POST['sample_id']
		if kw is not None:
			samples = Sample.objects.filter(barcode_no__icontains=kw)
			return render_to_response('samples/search_results.html', locals())

def delete(request, id):
	sample = Sample.objects.get(id=id)
	subject = sample.subject
	user = request.user
	if request.method == 'POST':
		# delete all analyses of that sample
		analysis_models.AnalysisAttribute.objects.filter(sample=sample).delete()
		# delete the sample
		sample.delete()
		return HttpResponseRedirect('/samples/list/bysubject/%s/1' % subject.id)
	return render_to_response('samples/delete.html', locals())

def add_aliquot(request, sample_id):
	if request.method == 'POST':
		sample = Sample.objects.get(id=sample_id)
		sample.aliquot_no = sample.aliquot_no + 1
		sample.save()
		return HttpResponse(sample.aliquot_no)
	return HttpResponse("-1")

def add_bookmark(request, sample_id):
	if request.method == 'POST':
		sample = Sample.objects.get(id=sample_id)
		sample.subscribers.add( request.user )
		return HttpResponse(request.user.id)

def remove_bookmark(request, sample_id):
	if request.method == 'POST':
		user = request.user
		sample = Sample.objects.get(id=sample_id)
		sample.subscribers.remove( request.user )
		return HttpResponse(True)

def show_bookmarks(request, page_num=1):
	user = request.user
 	paginator = Paginator(user.sample_bookmarks.all(), 10)
	page = paginator.page(page_num)
	bookmarks = page.object_list
	return render_to_response('samples/mysamplebookmarks.html', locals())
