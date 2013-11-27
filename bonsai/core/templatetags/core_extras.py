from django import template
from core import models

register = template.Library()

def is_in_list(value, arg):
	if value is None:
		return False
	if arg in value:
		return True
	return False

def sample_count(value):
	"""Returns the number of samples for a specific project."""
	return models.Sample.objects.filter(subject__project=value).count()

register.filter('is_in_list', is_in_list)
register.filter('is_in_subject_bookmarks', is_in_list)
register.filter('is_in_sample_bookmarks', is_in_list)
register.filter('sample_count', sample_count)
