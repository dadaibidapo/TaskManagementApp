from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Task

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView #login authentication view
from django.contrib.auth.mixins import LoginRequiredMixin



from django.contrib.auth.forms import UserCreationForm
# from django.views.generic.edit import FormView
from .models import CustomRegistrationForm
from django.contrib.auth import login
# Create your views here.

# def index(request):
#     tasks = Task.objects.all()
#     context = {'tasks': tasks}
#     return render(request, 'myTodo/index.html', context)



# ================================================================
class LoginPage(LoginView):
    template_name = "myTodo/login_page.html"
    fields = '__all__'
    redirect_authenticated_user =True
    # success_url = reverse_lazy('tasks')
    
    def get_success_url(self):
        return reverse_lazy('tasks')


class CustomRegistrationView(FormView):
    template_name = 'myTodo/registration_form.html'
    form_class = CustomRegistrationForm
    # form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')  # Redirect to the login page on successful registration

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegistrationView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(CustomRegistrationView, self).get(*args, **kwargs)


    # def form_valid(self, form):
    #     # Custom logic for successful form submission
    #     # Save the user and additional data
    #     user = form.save()
    #     user.save()

    #     # You can process additional fields here, e.g., user.first_name, user.last_name, user.email

    #     return super(CustomRegistrationView, self).form_valid(form)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "myTodo/index.html"
    context_object_name= 'tasks'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        
        context['count'] = context['tasks'].filter(complete = False).count()

        search_text = self.request.GET.get('search-area') or ''
        search_calendar = self.request.GET.get('calendar-date') or ''
        
        # context['search_text'] = search_text
        # context['search_calendar'] = search_calendar

        if search_text:
            context['tasks'] = context['tasks'].filter(title__startswith=search_text)

        if search_calendar:
            context['tasks'] = context['tasks'].filter(date_complete=search_calendar)

        return context
    


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "myTodo/showdetail.html"
    context_object_name= 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "myTodo/input_form.html"
    fields = ['title','description','date_complete', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = "myTodo/input_form.html"
    fields = ['title','description','date_complete', 'complete']
    success_url = reverse_lazy('tasks')
    context_object_name= 'task'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name= 'task'
    success_url = reverse_lazy('tasks')
    template_name = "myTodo/confirm_delete.html"