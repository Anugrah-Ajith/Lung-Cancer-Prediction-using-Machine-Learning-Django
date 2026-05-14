"""
URL configuration for predictor app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('predict/', views.predict_view, name='predict'),
    path('results/', views.results_view, name='results'),
]
