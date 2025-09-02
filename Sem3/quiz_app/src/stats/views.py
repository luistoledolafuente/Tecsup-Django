from django.shortcuts import render
from .models import Attempt
from quiz.models import Exam
from django.db import models

def stats_dashboard(request):
    attempts = Attempt.objects.all()
    avg_score = attempts.aggregate(models.Avg('score'))['score__avg'] or 0
    avg_time = attempts.aggregate(models.Avg('time_taken'))['time_taken__avg'] or 0
    exams = Exam.objects.all()
    exam_stats = []
    for exam in exams:
        exam_attempts = attempts.filter(exam=exam)
        fail_questions = {}  
        exam_stats.append({
            'exam': exam,
            'attempts': exam_attempts.count(),
            'avg_score': exam_attempts.aggregate(models.Avg('score'))['score__avg'] or 0,
            'avg_time': exam_attempts.aggregate(models.Avg('time_taken'))['time_taken__avg'] or 0,
            'fail_questions': fail_questions,
        })
    return render(request, 'stats/dashboard.html', {
        'avg_score': avg_score,
        'avg_time': avg_time,
        'exam_stats': exam_stats,
    })
