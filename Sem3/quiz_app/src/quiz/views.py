from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet
from categories.models import Category
from datetime import timedelta
from stats.models import Attempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


@login_required
def exam_submit(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        total_questions = exam.questions.count()
        correct_answers = 0
        failed_questions = []
        for question in exam.questions.all():
            correct_choice = question.choices.filter(is_correct=True).first()
            user_choice_id = request.POST.get(f'question_{question.id}')
            if correct_choice and str(correct_choice.id) == user_choice_id:
                correct_answers += 1
            else:
                failed_questions.append(question)
        score = correct_answers
        time_taken_seconds = int(request.POST.get('time_taken', 0))
        attempt = Attempt.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            time_taken=timedelta(seconds=time_taken_seconds)
        )
        attempt.failed_questions.set(failed_questions)
        attempt.save()
        messages.success(request, "¡Intento registrado!")
        return redirect('exam_detail', exam_id=exam.id)
    else:
        return redirect('exam_detail', exam_id=exam.id)
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('exam_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def exam_list(request):
    category_id = request.GET.get('category')
    exams = Exam.objects.all()
    categories = Category.objects.all()
    if category_id:
        exams = exams.filter(categories__id=category_id)
    return render(request, 'quiz/exam_list.html', {'exams': exams, 'categories': categories})

def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().prefetch_related('choices')
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})

def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.save()
            form.save_m2m()
            new_name = form.cleaned_data.get('new_category_name')
            if new_name:
                new_cat = Category.objects.create(
                    name=new_name,
                    description=form.cleaned_data.get('new_category_description', ''),
                    icon=form.cleaned_data.get('new_category_icon', '')
                )
                exam.categories.add(new_cat)
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'quiz/exam_form.html', {'form': form})

def question_create(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            with transaction.atomic():
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                formset = ChoiceFormSet(request.POST, instance=question)
                if formset.is_valid():
                    formset.save()
                    correct_count = question.choices.filter(is_correct=True).count()
                    if correct_count != 1:
                        messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                    else:
                        messages.success(request, 'Pregunta añadida correctamente.')
                    if 'add_another' in request.POST:
                        return redirect('question_create', exam_id=exam.id)
                    else:
                        return redirect('exam_detail', exam_id=exam.id)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()
    return render(request, 'quiz/question_form.html', {
        'exam': exam,
        'question_form': question_form,
        'formset': formset,
    })