"""Overwrite and add settings specifically for production deployed instance."""
from reciprocity.settings import *

DEBUG = False
ALLOWED_HOSTS.append('.us-west-2.compute.amazonaws.com')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = ()
