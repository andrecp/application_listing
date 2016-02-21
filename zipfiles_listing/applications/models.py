# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField(null=True, blank=True)
    file_path = models.FileField(upload_to='uploaded_files')
    description = models.TextField(max_length=5000)
    is_private = models.BooleanField(default=True)

    # LifeCycle properties.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Application, self).save(*args, **kwargs)
        if not self.url:
            self.url = '/{}'.format(self.id)
            self.save()
