from django.urls import path
from .views import category_stats

urlpatterns = [
    path('stats/', category_stats, name='category_stats'),
]