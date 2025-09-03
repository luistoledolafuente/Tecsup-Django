from django.shortcuts import render
from .models import Category

def category_stats(request):
    categories = Category.objects.all()
    stats = []
    for cat in categories:
        stats.append({'category': cat, 'exam_count': cat.exams.count()})
    return render(request, 'categories/stats.html', {'stats': stats})