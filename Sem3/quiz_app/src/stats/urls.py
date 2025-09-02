from django.urls import path
from .views import stats_dashboard

urlpatterns = [
    path('dashboard/', stats_dashboard, name='stats_dashboard'),
]