from django import forms
from models import Project, Subject, Sample, UserProfile
from django.conf import settings
import widgets
#from django.contrib.formtools.wizard import FormWizard

class ProjectForm(forms.ModelForm):
	description = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Project
		exclude = ['date_time_last_updated', 'last_updated_by', 'subscribers']
class SubjectForm (forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['project', 'donor_id', 'gender', 'age']

class SampleForm (forms.ModelForm):
	split_widget = forms.SplitDateTimeWidget()
	def __init__(self, data=None, **keyw):
		super(SampleForm, self).__init__(data, **keyw)
		self.split_widget.widgets[0].attrs = {'class': 'vDateField'}
		self.split_widget.widgets[1].attrs = {'class': 'vTimeField'}
	date_time_collected = forms.SplitDateTimeField(widget=split_widget, required=False)
	date_time_destroyed = forms.SplitDateTimeField(widget=split_widget, required=False)
	date_time_frozen = forms.SplitDateTimeField(widget=split_widget, required=False)

	class Meta:
		model = Sample
		exclude = ['aliquot_no', 'date_time_last_updated', 'last_updated_by', 'subscribers']

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user']							