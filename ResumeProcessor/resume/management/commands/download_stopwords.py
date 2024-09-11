# resume/management/commands/download_stopwords.py
from django.core.management.base import BaseCommand
import nltk

class Command(BaseCommand):
    help = 'Download NLTK stopwords'

    def handle(self, *args, **kwargs):
        nltk.download('stopwords')
        self.stdout.write(self.style.SUCCESS('Successfully downloaded NLTK stopwords'))
