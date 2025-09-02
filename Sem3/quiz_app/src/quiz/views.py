from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet
from categories.models import Category

def exam_list(request):
    category_id = request.GET.get('category')
    exams = Exam.objects.all()
    categories = Category.objects.all()
    if category_id:
        exams = exams.filter(categories__id=category_id)
    return render(request, 'quiz/exam_list.html', {'exams': exams, 'categories': categories})

def exam_detail(request, exam_id):
    """View to display the details of an exam with its questions"""
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
            # Crear nueva categoría si se ingresó
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
    """View to add questions to an exam"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            with transaction.atomic():
                # Save the question
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                
                # Process the formset for choices
                formset = ChoiceFormSet(request.POST, instance=question)
                if formset.is_valid():
                    formset.save()
                    
                    # Verify that only one option is marked as correct
                    correct_count = question.choices.filter(is_correct=True).count()
                    if correct_count != 1:
                        messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                    else:
                        messages.success(request, 'Pregunta añadida correctamente.')
                        
                    # Decide where to redirect
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
