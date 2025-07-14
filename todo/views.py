from django.shortcuts import render,redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def public_home(request):
    return render(request, 'todo/public_home.html')
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    return render(request,'todo/task_list.html',{'tasks':tasks, 'form':form} )

@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task,pk=pk, user=request.user)
        task.delete()
    return redirect('task_list')

#logout view
from django.contrib.auth import logout
from django.shortcuts import redirect
def custom_logout_view(request):
    logout(request)
    return redirect('home')

#login view
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')  # or '/' if you prefer

#signup view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form':form})