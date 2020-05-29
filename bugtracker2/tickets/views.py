from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
# Create your views here.
from . import models
from . import forms
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

User = get_user_model()

class TicketList(SelectRelatedMixin,generic.ListView):
    model = models.Ticket
    select_related = ('user', 'project')

class UserTickets(generic.ListView):
    model = models.Ticket
    template_name = 'tickets/user_ticket_list.html'

    def get_queryset(self):
        try:
            self.ticket_user = User.objects.prefetch_related('tickets').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.ticket_user.tickets.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_user'] = self.ticket_user
        return context

class TicketDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Ticket
    select_related = ('user','project')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreateTicket(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('message', 'project')
    model = models.Ticket

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeleteTicket(UserPassesTestMixin, LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Ticket
    select_related = ('user','project')
    success_url = reverse_lazy('tickets:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Ticket Deleted')
        return super().delete(*args,**kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.add_message(self.request, messages.INFO, 'Not enough permissions to delete a ticket')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
