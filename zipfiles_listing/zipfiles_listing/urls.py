"""zipfiles_listing URL Configuration. """

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import (
    url,
    include)

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^', include('applications.urls', namespace='applications')),
]

# We serve MEDIA files when in development mode to make life easier.
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
