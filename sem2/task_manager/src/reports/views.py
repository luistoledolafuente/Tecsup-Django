from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from tasks.models import Task
from django.contrib.auth.models import User
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    # Estadísticas generales
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    
    # Tareas por prioridad
    high_priority = Task.objects.filter(priority='high').count()
    medium_priority = Task.objects.filter(priority='medium').count()
    low_priority = Task.objects.filter(priority='low').count()
    
    # Tareas del usuario actual
    user_total = Task.objects.filter(created_by=request.user).count()
    user_completed = Task.objects.filter(created_by=request.user, status='completed').count()
    
    # Tareas recientes
    last_week = datetime.now() - timedelta(days=7)
    recent_tasks = Task.objects.filter(created_date__gte=last_week).count()
    
    # Progreso del usuario
    user_progress = 0
    if user_total > 0:
        user_progress = round((user_completed / user_total) * 100, 1)
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'user_total': user_total,
        'user_completed': user_completed,
        'user_progress': user_progress,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'reports/dashboard.html', context)

@login_required
def user_report(request):
    user = request.user
    user_tasks = Task.objects.filter(created_by=user)
    
    stats = {
        'total': user_tasks.count(),
        'completed': user_tasks.filter(status='completed').count(),
        'pending': user_tasks.filter(status='pending').count(),
        'in_progress': user_tasks.filter(status='in_progress').count(),
        'high_priority': user_tasks.filter(priority='high').count(),
    }
    
    return render(request, 'reports/user_report.html', {
        'user': user,
        'stats': stats,
        'tasks': user_tasks[:5]  # Últimas 5 tareas
    })