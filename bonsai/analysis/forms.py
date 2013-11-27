from django import forms
from models import AnalysisType
from django.shortcuts import render_to_response
from core.models import Sample
from models import AnalysisType, AnalysisAttribute

class AddAnalysisForm(forms.ModelForm):
	class Meta:
		model = AnalysisAttribute
		fields = ['name', 'value', 'analysis_type', 'sample', 'aliquot_id',]

class AddAnalysisTypeForm(forms.ModelForm):
	class Meta:
		model = AnalysisType
		fields = ['name', 'protocol_url', 'description']
