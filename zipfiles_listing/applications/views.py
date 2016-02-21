from django.shortcuts import render

from django.views.generic import View

from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404

from .forms import CreateApplicationForm
from .models import Application
from . import services as s

from django.http import HttpResponseForbidden


def edit_view(request, uid):

    # Unpack.
    user = request.user
    template_name = 'applications/edit_application.html'

    # Must be logged in to edit.
    if not user.is_authenticated():
        return HttpResponseForbidden()

    # Try to get the application.
    application = get_object_or_404(Application, pk=uid)

    # Verify if the user can edit.
    if not user == application.user:
        msg = 'This application does not belong to you'
        return HttpResponseForbidden(msg)

    form = CreateApplicationForm(instance=application)
    return render(request, template_name, {'form': form, 'uid': uid})


class ApplicationView(View):
    template_name = 'applications/application.html'
    form_class = CreateApplicationForm

    def get(self, request, uid):

        # Unpack.
        user = request.user

        # Try to get the application.
        application = get_object_or_404(Application, pk=uid)

        # If it is private we check if we got the right user.
        if application.is_private:
            if not (user.is_authenticated() and user == application.user):
                msg = 'This application is private and you are not logged in as the right user'
                return HttpResponseForbidden(msg)

        # Get data to the template.
        data = {'app': application}
        return render(request, self.template_name, data)

    def post(self, request, uid):

        # Unpack.
        user = request.user

        # Must be logged in to edit.
        if not user.is_authenticated():
            return HttpResponseForbidden()

        # Try to get the application.
        application = get_object_or_404(Application, pk=uid)

        # Verify if the user can edit.
        if not user == application.user:
            msg = 'This application does not belong to you'
            return HttpResponseForbidden(msg)

        form = self.form_class(request.POST, request.FILES, instance=application)

        # Verify if the form is valid.
        if form.is_valid():
            # Save the object.
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect(reverse('applications:application', args=[uid]))

        return render(request, self.template_name, {'form': form})


class ApplicationsView(View):
    form_class = CreateApplicationForm
    template_name = 'applications/index.html'

    def get(self, request, *args, **kwargs):

        # Unpack.
        user = request.user
        form = self.form_class()

        # Retrieve public and private applications.
        public_applications = s.public_applications()
        if user.is_authenticated():
            private_applications = s.private_applications(user)
        else:
            private_applications = []

        # Template data.
        data = {
            'form': form,
            'public_applications': public_applications,
            'private_applications': private_applications
        }

        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('You must be authenticated to create an application')
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Save the object.
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            uid = application.id
            return redirect(reverse('applications:application', args=[uid]))

        return render(request, self.template_name, {'form': form})
