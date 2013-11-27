	# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from core.models import Sample, Subject, Project
import forms
import datetime
import models
from django.utils import simplejson
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator


def main_view(request, sample_id):
	user = request.user
	sample = Sample.objects.get(id=sample_id)
	return render_to_response('analysis/main.html', locals())

def main_add(request, sample_id):
	sample = Sample.objects.get(id=sample_id)
	return render_to_response('analysis/main_add.html', locals())

def main_manage(request, sample_id):
	sample = Sample.objects.get(id=sample_id)
	return render_to_response('analysis/main_manage.html', locals())

def add_analysis(request, sample_id):
	sample = Sample.objects.get(id=sample_id)
	if request.method == 'POST':
		attr = models.AnalysisAttribute(sample=sample,
			date_time_last_updated=datetime.datetime.now(), last_updated_by=request.user)
		form = forms.AddAnalysisForm(request.POST, instance=attr)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/analysis/main/%s' % sample_id)
	form = forms.AddAnalysisForm()
	analysed_aliquots = models.AnalysisAttribute.objects.filter(sample__id=sample_id).values('aliquot_id')
	# purify the ids into a list
	vals = [ aa['aliquot_id'] for aa in analysed_aliquots]
	print vals
	aliquot_dict = {}
	# Free: true
	# Analysed: false
	for i in range(1,sample.aliquot_no+1): # +1: because aliquot numbers start from one not zero.
		aliquot_dict[i] = str(i) not in vals
	print aliquot_dict
	return render_to_response('analysis/analysis_add.html', locals())

def add_analysis_type(request):
	if request.method == 'POST':
		atype = models.AnalysisType(date_time_last_updated=datetime.datetime.now(), last_updated_by=request.user)
		form = forms.AddAnalysisTypeForm(request.POST, instance=atype)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/analysis/attr/add')
	analysis_type_form = forms.AddAnalysisTypeForm()
	return render_to_response('analysis/analysis_type_add.html', locals())

def add(request):
	form = forms.AddAnalysisForm()
	if request.method == 'POST':
		attr = models.AnalysisAttribute(date_time_last_updated=datetime.datetime.now(), last_updated_by=request.user)
		form = forms.AddAnalysisForm(request.POST, instance=attr)
		if form.is_valid():
			form.save()
			# update sample i.e. increase aliquot number by one
			sample = form.instance.sample
			if sample.aliquot_no is None:
				sample.aliquot_no = 1
			else:
				sample.aliquot_no = sample.aliquot_no + 1
			sample.save()
			success = True

	subscribed_projects = request.user.project_subscriptions.all()
	form.fields['sample'].queryset = Sample.objects.filter(subject__project__in=subscribed_projects)
	return render_to_response('analysis/add_attr.html', locals())

def get_sample_attributes(request, sample_id):
	q = request.GET['q']
	analysis_attributes = models.AnalysisAttribute.objects.filter(name__icontains=q, sample__id=sample_id).values('name').distinct()
	name_list = [attr['name'] + '\n' for attr in analysis_attributes]
	return HttpResponse(name_list)

def get_attributes_by_analysis_type(request, analysis_type_id):
	q = request.GET['q']
	if q == '*':
		analysis_attributes = models.AnalysisAttribute.objects.all().values('name').distinct()
	else:
		analysis_attributes = models.AnalysisAttribute.objects.filter(name__icontains=q, analysis_type__id__exact=analysis_type_id).values('name').distinct()
	name_list = [attr['name'] + '\n' for attr in analysis_attributes]
	return HttpResponse(name_list)

def show_by_sample(request, sample_id, page_num=1):
	""" Lists all the analysis page by page """
	sample = Sample.objects.get(id=sample_id)
	query = models.AnalysisAttribute.objects.filter(sample=sample)
	filtered = False
	if 'showvalue' in request.GET and request.GET['showvalue']:
		query = query.filter(value__isnull=False)		
		filtered=True
	paginator = Paginator(query.order_by('-date_time_last_updated'), 10)
	page = paginator.page( page_num )
	analyses = page.object_list
	return render_to_response('analysis/show_by_sample.html', locals())

def edit(request, analysis_id):
	user = request.user
	subscriptions = user.project_subscriptions.all()
	analysis = models.AnalysisAttribute.objects.get(id=analysis_id)
	if request.method == 'POST':
		analysis.date_time_last_updated=datetime.datetime.now()
		analysis.last_updated_by=user
		form = forms.AddAnalysisForm(request.POST, instance=analysis)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/analysis/show/bysample/%s/1' % analysis.sample.id)
	form = forms.AddAnalysisForm(instance=analysis)
	return render_to_response('analysis/edit.html', locals())

def delete(request, analysis_id):
	user = request.user
	analysis = models.AnalysisAttribute.objects.get(id=analysis_id)
	if request.method == 'POST':
		sample_id = analysis.sample.id
		if analysis.sample.aliquot_no is not None:
			analysis.sample.aliquot_no = analysis.sample.aliquot_no - 1
			analysis.sample.save()
		analysis.delete()
		return HttpResponseRedirect('/analysis/show/bysample/%s/1' % sample_id)
	return render_to_response('analysis/delete.html', locals())

