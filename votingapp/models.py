from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# models created from tutorial from w3schools

#Election Model
class Election(models.Model):
    election_type = models.CharField(max_length=125)
    date = models.DateTimeField()
    start_time= models.DateTimeField()
    end_time = models.DateTimeField()
  
#Voter Model
class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

#Candidates Model
class Candidate(models.Model):
    name = models.CharField(max_length=275)
    photo = models.ImageField(upload_to="uploads/", max_length=150)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

#Votes Model
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)




