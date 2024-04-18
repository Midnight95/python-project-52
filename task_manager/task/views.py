from task_manager.task.models import Task
from task_manager.task.forms import TaskForm
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.myxini import LoginCheckMixin


class TaskListView(LoginCheckMixin, ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    extra_context = {'title': _('Task list')}


class TaskView(LoginCheckMixin, DeleteView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'
    extra_context = {'title': _('Task view')}


class TaskCreateView(LoginCheckMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'forms/form.html'
    extra_context = {
        'title': _('Create task'),
        'button_text': _('Create')
        }
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginCheckMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'forms/form.html'
    extra_context = {
        'title': _('Change task'),
        'button_text': _('Submit'),
    }
    success_message = _('Task updated successfully')
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginCheckMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'forms/delete.html'
    success_message = _('Task deleted successfully')
    extra_context = {
        'title': _('Delete task'),
        'button_text': _('Delete')
    }
    success_url = reverse_lazy('task_list')
