from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher
from django.db.models.signals import post_save
from signals import send_sample_created_email

# -------------------
# Lookup Models
# -------------------
class ProjectCode(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class CollectionMethod(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=45)
    def __unicode__(self):
        return self.name

class StorageMethod(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name


# -------------------
# Core Models
# -------------------

class Project(models.Model):
    description = models.CharField(max_length=255, null=True, blank=True)
    date_time_last_updated = models.DateTimeField()
    dms_link = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    foliotracker_link = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    last_updated_by = models.ForeignKey(User)
    project_code = models.ForeignKey(ProjectCode, verbose_name="* Project code")
    subscribers = models.ManyToManyField(User, related_name="project_subscriptions")
    def __unicode__(self):
        return self.project_code.name

class Subject(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('(NA)', '(NA)'),
    )
    project = models.ForeignKey(Project, related_name='subjects', verbose_name="* Project")
    donor_id = models.CharField(max_length=45, null=True, blank=True)
    age = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    date_time_last_updated = models.DateTimeField()
    gender = models.CharField(max_length=4, choices = GENDER_CHOICES, verbose_name="* Gender")
    last_updated_by = models.ForeignKey(User)
    subscribers = models.ManyToManyField(User, related_name="subject_bookmarks")
    def __unicode__(self):
        return self.donor_id

class Sample(models.Model):
    aliquot_no = models.IntegerField()
    subject = models.ForeignKey(Subject, related_name='samples', blank=True, null=True)
    barcode_no = models.CharField(max_length=45, verbose_name="* Barcode no")
    collection_method = models.ForeignKey(CollectionMethod, blank=True, null=True)
    date_time_collected = models.DateTimeField(blank=True,null=True)
    date_time_destroyed = models.DateTimeField(null=True, blank=True)
    date_time_frozen = models.DateTimeField(null=True, blank=True)
    date_time_last_updated = models.DateTimeField()
    dms_sample_info_sheet_link = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    external_sample_id = models.CharField(max_length=255, blank=True,null=True)
    freezer_location = models.CharField(max_length=20, null=True, blank=True)
    freeze_method = models.CharField(max_length=20, blank=True, null=True)
    last_updated_by = models.ForeignKey(User)
    material = models.ForeignKey(Material, blank=True, null=True)
    storage_method = models.ForeignKey(StorageMethod, blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name="sample_bookmarks")
    def __unicode__(self):
        return self.barcode_no

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    list_per_page = models.IntegerField()


# Signal connecting
# post_save.connect(send_sample_created_email, sender=Sample)
