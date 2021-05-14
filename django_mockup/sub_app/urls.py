from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main_home' ),
    path( 'questions/', views.questions, name='main_questions' ),
    path( 'tempview/', views.view_agreement1, name='main_view_agreement1' ),
    path( 'downloads/', views.scraper, name='main_scraper' ),
    path( 'users_data/', views.CSVFileView.as_view(), name='csv_download' )
]
