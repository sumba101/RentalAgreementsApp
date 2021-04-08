from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main_home' ),
    path( 'questions/', views.questions, name='main_questions' ),
    path('results/', views.result, name='main_result' ),
]
