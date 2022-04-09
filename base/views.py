from queue import Empty
from re import template
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']= context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model =Task
    context_object_name ='task'
    def get_queryset(self):
        user = self.request.user

        task = self.model.objects.filter(user=self.request.user)
        print(task)
        print(self.model.objects.all().values('user'))
        return task

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

# Overrides get_queryset to show 404 if user is not author of task
class TaskUpdate(LoginRequiredMixin, UpdateView ):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )
    
# Uses the UserPassesTestMixin and test_func method to send invalid user to 403
class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False