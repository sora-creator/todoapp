from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Task, List
from .forms import TaskForm

class TaskListView(ListView):
    model = Task
    template_name = 'todoapp/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10  # 페이지당 10개의 항목

    def get_queryset(self):
        queryset = Task.objects.all().order_by('-created_date')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lists'] = List.objects.all()
        context['query'] = self.request.GET.get('q', '')
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todoapp/add_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        # 필요한 경우 폼 처리 로직을 추가할 수 있습니다.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lists'] = List.objects.all()  # List 모델의 모든 객체를 컨텍스트에 추가
        return context

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'todoapp/edit_task.html'
    success_url = reverse_lazy('task_list')

    def get_object(self, queryset=None):
        """ 현재 사용자와 연관된 Task 객체를 반환 """
        obj = get_object_or_404(Task, pk=self.kwargs['pk'])
        return obj

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'todoapp/delete_task.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_title'] = self.object.title
        return context

