from django.shortcuts import render
from django.db.models import Avg, Count, F
from .models import Attempt
from quiz.models import Exam, Question
from django.contrib.auth.models import User

def stats_dashboard(request):
    attempts = Attempt.objects.all()
    avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    avg_time = attempts.aggregate(Avg('time_taken'))['time_taken__avg'] or 0

    # Formatea tiempo promedio en minutos y segundos
    if avg_time:
        total_seconds = int(avg_time.total_seconds())
        avg_time_str = f"{total_seconds // 60} min {total_seconds % 60} seg"
    else:
        avg_time_str = "0 min 0 seg"

    # Estadísticas por examen
    exams = Exam.objects.all()
    exam_stats = []
    for exam in exams:
        exam_attempts = attempts.filter(exam=exam)
        exam_avg_score = exam_attempts.aggregate(Avg('score'))['score__avg'] or 0
        exam_avg_time = exam_attempts.aggregate(Avg('time_taken'))['time_taken__avg'] or 0
        if exam_avg_time:
            exam_seconds = int(exam_avg_time.total_seconds())
            exam_avg_time_str = f"{exam_seconds // 60} min {exam_seconds % 60} seg"
        else:
            exam_avg_time_str = "0 min 0 seg"
        exam_stats.append({
            'exam': exam,
            'attempts': exam_attempts.count(),
            'avg_score': exam_avg_score,
            'avg_time': exam_avg_time_str,
        })

    # Preguntas con más fallos (global)
    question_fail_count = {}
    for attempt in attempts:
        for question in attempt.failed_questions.all():
            question_fail_count[question.id] = question_fail_count.get(question.id, 0) + 1
    top_failed_questions = sorted(
        [(Question.objects.get(id=qid), count) for qid, count in question_fail_count.items()],
        key=lambda x: x[1], reverse=True
    )[:5]

    # Estadísticas por usuario
    user_stats = []
    for user in User.objects.all():
        user_attempts = attempts.filter(user=user)
        if user_attempts.exists():
            user_avg_score = user_attempts.aggregate(Avg('score'))['score__avg'] or 0
            user_avg_time = user_attempts.aggregate(Avg('time_taken'))['time_taken__avg'] or 0
            if user_avg_time:
                user_seconds = int(user_avg_time.total_seconds())
                user_avg_time_str = f"{user_seconds // 60} min {user_seconds % 60} seg"
            else:
                user_avg_time_str = "0 min 0 seg"
            user_percent = round((user_attempts.aggregate(Avg('correct_answers'))['correct_answers__avg'] or 0) / (user_attempts.aggregate(Avg('total_questions'))['total_questions__avg'] or 1) * 100, 2)
            user_stats.append({
                'user': user,
                'attempts': user_attempts.count(),
                'avg_score': user_avg_score,
                'avg_time': user_avg_time_str,
                'percent': user_percent,
            })

    return render(request, 'stats/dashboard.html', {
        'avg_score': avg_score,
        'avg_time': avg_time_str,
        'exam_stats': exam_stats,
        'top_failed_questions': top_failed_questions,
        'user_stats': user_stats,
    })