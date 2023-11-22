from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# models created from tutorial from w3schools
#Election Model for creatinng the election table
# in the database
class Election(models.Model):
    election_type = models.CharField(max_length=125)
    date = models.DateField()
    start_time= models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
  
  
#Voter Model
#For creating the Voter table in the database
class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)

#Candidates Model

class Candidate(models.Model):
    name = models.CharField(max_length=275)
    bio = models.TextField(max_length=13, default=False)
    photo = models.ImageField(upload_to="candidates/", max_length=150)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

#Votes Model
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=False)




