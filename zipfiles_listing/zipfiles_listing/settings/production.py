# -*- coding: utf-8 -*-
from .base import *

import os
# Update database configuration with $DATABASE_URL.
import dj_database_url

# XXX Using this intead of DEBUG just because it's a demo
# and easier to deploy to heroku and mange media files...
RUNNING_LOCALLY = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            'jiz8x9cav0_+yr1i7l)bbj0)i)ifdq@ra)*y73g=r#pcz&0y#^')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = ['murmuring-eyrie-70574.herokuapp.com']
