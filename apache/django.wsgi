import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/harken/harken/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/harken/harken/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'harken.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
