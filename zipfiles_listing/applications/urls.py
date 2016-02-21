
from django.conf.urls import url

from . import views as v

urlpatterns = [
    url(r'^$', v.ApplicationsView.as_view(), name='list'),
    url(r'^(?P<uid>[0-9]+)$', v.ApplicationView.as_view(), name='application'),
    url(r'^(?P<uid>[0-9]+)/edit$', v.edit_view, name='edit_application')
]
