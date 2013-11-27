# Django settings for mysite project.
import logging 
import os
APPEND_SLASH=True
#AUTHENTICATION_BACKENDS=("mysite.myauth.SettingsBackend",)
SESSION_EXPIRE_AT_BROWSER_CLOSE =True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'data.sqlite'
    }
}
# DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
# DATABASE_NAME = 'data.db3'             # Or path to database file if using sqlite3.
# DATABASE_USER = ''             # Not used with sqlite3.
# DATABASE_PASSWORD = ''         # Not used with sqlite3.
# DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
# DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
#TIME_ZONE = 'America/Chicago'
TIME_ZONE ='Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE="cn"

SITE_ID = 2

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.split(__file__)[0]+"/media/"

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.split(__file__)[0]+"/../staticRoot/"
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/site_media/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.split(__file__)[0]+"/../static/",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = '$=9%g!ie727#n4lo+nzgud%3plnk5u^6yd&c@$z+*h*2pv4z_^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
os.path.split(__file__)[0]+"/../templates/"
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
)

INSTALLED_APPS = (
   
    'django.contrib.markup',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'core',
    'analysis',
)
#myconfig_download=r"./tgphoto"
#download_dir="./tgdownload/"
#WORKSTYLE_MEDIA_ROOT="./static"
logging.basicConfig(  
    level = logging.DEBUG,   
    #  
    format = '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s',  
    #filename = 'filelog.log',  
)  
AUTH_PROFILE_MODULE = "core.userprofile"