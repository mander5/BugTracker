from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from . import models
from django.db import IntegrityError
from projects.models import Project,ProjectMember
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
class CreateProject(LoginRequiredMixin,UserPassesTestMixin,generic.CreateView):
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        messages.add_message(self.request, messages.INFO, 'Not enough permissions to create a project')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    fields = ('name','description')
    model = Project

class SingleProject(generic.DetailView):
    model = Project

class ListProject(generic.ListView):
    model = Project

class JoinProject(LoginRequiredMixin,UserPassesTestMixin, generic.RedirectView):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.add_message(self.request, messages.INFO, 'Not enough permissions to join a project')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def get_redirect_url(self, *args, **kwargs):
        return reverse("projects:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project,slug=self.kwargs.get("slug"))

        try:
            ProjectMember.objects.create(user=self.request.user,project=project)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(project.name)))

        else:
            messages.success(self.request,"You are now a member of the {} project.".format(project.name))

        return super().get(request, *args, **kwargs)


class LeaveProject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("projects:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.ProjectMember.objects.filter(
                user=self.request.user,
                project__slug=self.kwargs.get("slug")
            ).get()

        except models.ProjectMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this project because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this project."
            )
        return super().get(request, *args, **kwargs)
