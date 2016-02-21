# Gunicorn configuration file
import os

bind = '0.0.0.0:{0}'.format(os.environ.get('PORT', 5100))

loglevel = 'INFO'
errorlog = '-'
accesslog = '-'
