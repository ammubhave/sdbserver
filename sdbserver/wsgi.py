"""
WSGI config for sdbserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/ambhave/.virtualenvs/sdbserver/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/ambhave/public_html/amolbhave.mit.edu')
sys.path.append('/home/ambhave/public_html/amolbhave.mit.edu/sdbserver')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdbserver.settings")

# Activate your virtual env
activate_env = os.path.expanduser("/home/ambhave/.virtualenvs/sdbserver/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
