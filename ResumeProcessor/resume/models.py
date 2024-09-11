from django.db import models

# Create your models here.
from django.db import models

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name
