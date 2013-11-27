from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from models import Project, Sample
import forms
import datetime
from django.core.paginator import Paginator
from django.utils import simplejson

def list(request, page_num):
	"""Lists all the projects."""
	# subscriptions are for starring subscribed projects.
	subscriptions = request.user.project_subscriptions.all()
	#  list_per_page: default 10
	list_per_page = request.user.get_profile().list_per_page
	paginator = Paginator( Project.objects.all().order_by('project_code__name'), list_per_page )
	page = paginator.page(page_num)
	projects = page.object_list
	return render_to_response('projects/list.html', locals() )

def list_subscribed(request):
	user = request.user
	subscriptions = user.project_subscriptions.all()
	return render_to_response('projects/list_subscribed.html', locals() )

def subscribe_user(request, project_id):
    project = Project.objects.get(id=project_id)
    project.subscribers.add(request.user)
    return HttpResponse(request.user.project_subscriptions.count())

def unsubscribe_user(request, project_id):
	project = Project.objects.get(id=project_id)
	project.subscribers.remove(request.user)
	return HttpResponse(request.user.project_subscriptions.count())

def notify_user(request, subscription_id):
	pass
	
def denotify_user(request, subscription_id):
	pass
	
def add(request):
	if request.method == 'POST':
		error = False
		p = Project()
		p.date_time_last_updated = datetime.datetime.now()
		p.last_updated_by = request.user
		form = forms.ProjectForm(request.POST, instance=p)
		if form.is_valid():
			form.save()			
		else:
			error = True
	projects = Project.objects.all().order_by('project_code')
	form = forms.ProjectForm()
	return render_to_response('projects/add.html', locals() )

def show(request, id):
	project = Project.objects.get(id=id)
	subjects = project.subjects.all().order_by('donor_id')
	return render_to_response('projects/show.html', locals())

def edit(request, id):	
	if request.method == 'POST':
		error = False
		p = Project.objects.get(id=id)
		p.date_time_last_updated = datetime.datetime.now()
		p.last_updated_by = request.user
		form = forms.ProjectForm(request.POST, instance=p)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/project/show/%s' % id)
		else:
			error = True
	project = Project.objects.get(id=id)
	subjects = project.subjects.all().order_by('donor_id')
	form = forms.ProjectForm(instance=project)
	return render_to_response('projects/edit.html', locals())

def delete(request, id):
	if request.method == 'POST':
		p = Project.objects.get(id=id)
		# recursively purging
		subjects = p.subjects.all()
		for subject in subjects:
			Sample.objects.filter(subject=subject).delete()
		subjects.delete()
		p.delete()
		return HttpResponseRedirect('/project/list/')
	project = Project.objects.get(id=id)
	subjects = project.subjects.all().order_by('donor_id')
	return render_to_response('projects/delete.html', locals())	

def samples(request, project_id, page_length, goto_page):
	project = Project.objects.get(id=project_id)
	subjects = project.subjects.all().order_by('donor_id')
	paginator = Paginator(Sample.objects.filter(subject__project=project), int(page_length) )
	try:
		page_items = paginator.page(int(goto_page))
	except EmptyPage:
		error = True		
	return render_to_response('projects/samples.html', locals())
	
def json_samples_by_project(request, id):
	#TODO refactor to a more elegant way
	subjects = Project.objects.get(id=id).subjects.all()
	sample_list = []
	for subject in subjects:
		samples = subject.samples.all()
		for sample in samples:
			sample_list.append(sample.json_value)
	return HttpResponse(simplejson.dumps(sample_list), mimetype="application/json")
	
def json_all_projects(request):
	projects = Project.objects.all().order_by('project_code')
	tree_data = {'label': 'name', 'identifier':'id', 'items':[]}
	
	for project in projects:
		project_data = { 'name': project.project_code.name, 'id':'project_%s' % str(project.id), 'type':'project', 'pk':project.id, 'icon':'bonsai_projectIcon' }
		subjects = project.subjects.all()
		if subjects.count() > 0:
			project_data['children'] = []
			for subject in subjects:
				subject_data = { 'name': subject.donor_id, 'id':'subject_%s' % str(subject.id), 'type':'subject', 'pk':subject.id, 'icon':'bonsai_subjectIcon' }
				samples = subject.samples.all()
				if samples.count() > 0:
					subject_data['children'] = []
					for sample in samples:
						sample_data = { 'name': sample.barcode_no, 'id':'sample_%s' % str(sample.id), 'type':'sample', 'pk':sample.id, 'icon':'bonsai_sampleIcon' }
						subject_data['children'].append(sample_data)
				project_data['children'].append(subject_data)
		tree_data['items'].append( project_data )		
	projects_json = simplejson.dumps(tree_data)	
	return HttpResponse(projects_json, 'application/javascript')

