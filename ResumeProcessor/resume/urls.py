from django.urls import path
from .views import ResumeExtractionView

urlpatterns = [
    path('extract_resume/', ResumeExtractionView.as_view(), name='extract_resume'),
]
