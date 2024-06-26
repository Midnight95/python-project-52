from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import LoginCheckMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView


class TaskPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user != self.get_object().author:
            self.permission_denied_message = _('Only author can delete task!')
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(reverse_lazy('tasks'))


class TaskListView(LoginCheckMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskView(LoginCheckMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginCheckMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/task_create_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task created successfully')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginCheckMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update_form.html'
    success_message = _('Task updated successfully')
    success_url = reverse_lazy('tasks')


class TaskDeleteView(
        TaskPermissionMixin,
        LoginCheckMixin,
        SuccessMessageMixin,
        DeleteView
):
    model = Task
    template_name = 'tasks/task_delete_form.html'
    success_message = _('Task deleted successfully')
    success_url = reverse_lazy('tasks')
