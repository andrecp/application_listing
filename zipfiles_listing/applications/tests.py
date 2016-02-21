# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Application
from . import services as s


def create_user(username='foo', email='a@b.c', password='bar'):
    return User.objects.create_user(username, email, password)


def create_application(user=None, is_private=True):
    if user is None:
        user = create_user()
    file_path = '/'
    description = 'this is a test'
    app = Application(
              user=user,
              is_private=is_private,
              file_path=file_path,
              description=description)
    app.save()
    return app


class UnitTests(TestCase):

    def test_services(self):
        """Check the public / private application logic."""

        user = create_user(username='1', email='b@a.b')
        app = create_application(user)
        self.assertTrue(app in s.private_applications(user))
        self.assertFalse(app in s.public_applications())
        app.is_private = False
        app.save()
        self.assertFalse(app in s.private_applications(user))
        self.assertTrue(app in s.public_applications())


class FunctionalTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Create an user.
        self.user = create_user()

    def test_create_application(self):
        """POST to / should create a new application"""

        applications_url = u'/'

        # Post a new application without being logged in.
        response = self.client.post(
                applications_url,
                {'file_path': '..', 'description': 'cool', 'is_private': False},
                content_type='multipart/form-data')

        # Should return 403 - Forbidden!
        self.assertEqual(403, response.status_code)

        # Log in..
        self.client.login(username='foo', password='bar')

        # Now it should work.
        file = SimpleUploadedFile('file.mp4', 'file_content', content_type='multipart/form-data')
        response = self.client.post(
                applications_url,
                {'file_path': file, 'description': 'cool', 'is_private': False},
                )

        self.assertEqual(302, response.status_code)


class ModelTests(TestCase):

    def test_create_application(self):
        """Basic application model tests."""

        user = create_user()
        file_path = '/'
        description = 'this is a test'
        app = Application(
                  user=user,
                  file_path=file_path,
                  description=description)
        app.save()

        # Check if db id is being generated.
        self.assertEqual(app.id, Application.objects.get().id)
        # Default privacy mode is private.
        self.assertTrue(Application.objects.get().is_private)
        # Auto generated url is the object is.
        self.assertEqual(Application.objects.get().url, '/' + str(app.id))
        # Check that both create and modified dates were set.
        self.assertTrue(Application.objects.get().created)
        self.assertTrue(Application.objects.get().modified)

