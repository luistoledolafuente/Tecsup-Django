from django.db import models
from django.contrib.auth.models import User
from quiz.models import Exam, Question

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    time_taken = models.DurationField()
    date = models.DateTimeField(auto_now_add=True)
    failed_questions = models.ManyToManyField(Question, blank=True)  

    def percent_correct(self):
        if self.total_questions:
            return round((self.correct_answers / self.total_questions) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} ({self.date})"