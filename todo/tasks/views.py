from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Task, Category
from .forms import TaskForm, TaskFilterForm


def index(request):
    category = request.GET.get('category')
    priority = request.GET.get('priority')
    filter_form = TaskFilterForm(initial={'category': category, 'priority': priority}, user=request.user)
    tasks = Task.objects.filter(done=False)
    if category:
        tasks = tasks.filter(category=category)
    if priority:
        tasks = tasks.filter(priority=priority)
    context = {'tasks': tasks,  'filter_form': filter_form}
    return render(request, 'task_list.html', context)


def category_tasks(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category, 'tasks': category.tasks.all()}
    return render(request, 'task_list.html', context)


def task_detail(request, category_slug, pk):
    category = get_object_or_404(Category, slug=category_slug)
    task = get_object_or_404(Task, pk=pk)
    context = {'task': task}
    return render(request, 'task_detail.html', context)


def task_create(request, task_id=None):
    # form = TaskForm(request.POST or None)
    task = None
    if task_id:
        task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if not task:
                task = form.save(commit=False)
                task.user = request.user
            task.save()
            return redirect(reverse('task_detail', kwargs={'category_slug': task.category.slug, 'pk': task.id}))
        return render(request, 'task_form.html', {'form': form})
    form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

