# -*- coding: utf-8 -*-
"""Application services"""

from .models import Application


def private_applications(user):
    """Returns the user's private applications ordered by created."""

    applications = Application.objects
    belonging_to_user = applications.filter(user=user)
    private_applications = belonging_to_user.filter(is_private=True)
    order_by_recent = private_applications.order_by('-created')
    return order_by_recent


def public_applications():
    """Returns the private applications ordered by created."""

    return Application.objects.filter(is_private=False).order_by('-created')
