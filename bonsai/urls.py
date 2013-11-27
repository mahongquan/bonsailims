from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from core import views
from core import project_views
from core import subject_views
from core import sample_views
from analysis import views as analysis_views
import settings
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
	# LOGIN/LOGOUT
    (r'^$', views.index),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^help/$', direct_to_template, {'template': 'help.html'}),
    (r'^user/logout/$', views.logout_user),
    (r'^user/settings/$', views.set_user_profile),
    (r'^user/subscribe/(?P<project_id>\d+)$', project_views.subscribe_user),
    (r'^user/unsubscribe/(?P<project_id>\d+)$', project_views.unsubscribe_user),
    (r'^user/subscription/notify/(?P<subscription_id>\d+)$', project_views.notify_user),
    (r'^user/subscription/denotify/(?P<subscription_id>\d+)$', project_views.denotify_user),
    (r'^subjects/list/(?P<project_id>\d+)/(?P<page_num>\d+)$', subject_views.show_by_project),
    (r'^subjects/list/byuser/(?P<page_num>\d+)$', subject_views.show_by_user),
    (r'^samples/list/byproject/(?P<project_id>\d+)/(?P<page_num>\d+)$', sample_views.show_by_project),
    (r'^samples/list/bysubject/(?P<subject_id>\d+)/(?P<page_num>\d+)$', sample_views.show_by_subject),
    (r'^samples/list/byuser/(?P<page_num>\d+)$', sample_views.show_by_user),
    #Bookmarks
    (r'^bookmark/subject/show/(?P<page_num>\d+)$', subject_views.show_bookmarks),
    (r'^bookmark/subject/add/(?P<subject_id>\d+)$', subject_views.add_bookmark),
    (r'^bookmark/subject/remove/(?P<subject_id>\d+)$', subject_views.remove_bookmark),
    (r'^bookmark/sample/show/(?P<page_num>\d+)$', sample_views.show_bookmarks),
    (r'^bookmark/sample/add/(?P<sample_id>\d+)$', sample_views.add_bookmark),
    (r'^bookmark/sample/remove/(?P<sample_id>\d+)$', sample_views.remove_bookmark),

    # CRUD
    (r'^project/list/(?P<page_num>\d+)$', project_views.list),
    (r'^project/list/subscribed$', project_views.list_subscribed),
    (r'^project/add/$', project_views.add),
    (r'^project/show/(\d+)$', project_views.show),
    (r'^project/edit/(\d+)$', project_views.edit),
    (r'^project/delete/(\d+)$', project_views.delete),
    (r'^project/show/samples/(?P<project_id>\d+)/(?P<page_length>\d+)/(?P<goto_page>\d+)', project_views.samples),
    (r'^subject/add/$', subject_views.add),
    (r'^subject/show/(\d+)$', subject_views.show),
    (r'^subject/edit/(\d+)$', subject_views.edit),
    (r'^subject/delete/(\d+)$', subject_views.delete),
    (r'^sample/add$', sample_views.add),
    (r'^sample/show/(\d+)$', sample_views.show),
    (r'^sample/edit/(\d+)$', sample_views.edit),
    (r'^sample/delete/(\d+)$', sample_views.delete),
    (r'^sample/search$', sample_views.search),
    (r'^sample/aliquot/new/(?P<sample_id>\d+)$', sample_views.add_aliquot),
    # JSON API
    (r'^json/project/get/(\d+)$', project_views.json_samples_by_project),
    (r'^json/projects/all/', project_views.json_all_projects),
    # ANALYSIS
    (r'^analysis/attr/add$', analysis_views.add),
    (r'^analysis/main/add/analysis/(?P<sample_id>\d+)', analysis_views.add_analysis),
    (r'^analysis/main/add/analysis_type$', analysis_views.add_analysis_type),
	(r'^analysis/main/manage/(?P<sample_id>\d+)', analysis_views.main_manage),
    (r'^analysis/bysample/(?P<sample_id>\d+)$', analysis_views.add ),
    (r'^analysis/main/(?P<sample_id>\d+)$', analysis_views.main_view ),
    (r'^analysis/show/bysample/(?P<sample_id>\d+)/(?P<page_num>\d+)$', analysis_views.show_by_sample ),
    (r'^analysis/attributes/bysample/(?P<sample_id>\d+)$', analysis_views.get_sample_attributes),
    (r'^analysis/attributes/byanalysis_type/(?P<analysis_type_id>\d+)$', analysis_views.get_attributes_by_analysis_type),
    (r'^analysis/edit/(?P<analysis_id>\d+)$', analysis_views.edit ),
    (r'^analysis/delete/(?P<analysis_id>\d+)$', analysis_views.delete ),
    # ADMIN
    url(r'^admin/', include(admin.site.urls)),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
)
urlpatterns += staticfiles_urlpatterns()
