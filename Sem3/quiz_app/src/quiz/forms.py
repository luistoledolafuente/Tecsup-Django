from django import forms
from .models import Exam, Question, Choice
from categories.models import Category

class ExamForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Categorías existentes"
    )
    new_category_name = forms.CharField(
        max_length=100, required=False, label="Nueva categoría"
    )
    new_category_description = forms.CharField(
        widget=forms.Textarea, required=False, label="Descripción de nueva categoría"
    )
    new_category_icon = forms.CharField(
        max_length=100, required=False, label="Icono de nueva categoría"
    )

    class Meta:
        model = Exam
        fields = ['title', 'description', 'categories']
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Crear formset para opciones
ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice, form=ChoiceForm, extra=4, can_delete=False
)
