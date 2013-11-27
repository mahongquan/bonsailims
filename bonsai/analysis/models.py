from django.db import models
from core import models as core_models

from django.contrib.auth.models import User

# Create your models here.
class AnalysisType(models.Model):
	name = models.CharField(max_length=30,verbose_name="* Name")
	description = models.CharField(max_length=30, null=True, blank=True)
	protocol_url = models.URLField(null=True, blank=True)
	date_time_last_updated = models.DateTimeField()
	last_updated_by = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

class AnalysisAttribute(models.Model):
	analysis_type = models.ForeignKey(AnalysisType, verbose_name="* Analysis type")
	sample = models.ForeignKey(core_models.Sample, related_name="analysis_attributes", verbose_name="* Sample")
	name = models.CharField(max_length=30, verbose_name="* Name")
	value = models.CharField(max_length=50, null=True, blank=True)
	aliquot_id = models.CharField(max_length=50, verbose_name="* Aliquot id")
	last_updated_by = models.ForeignKey(User)
	date_time_last_updated = models.DateTimeField()
	def  __unicode__(self):
		return self.name

