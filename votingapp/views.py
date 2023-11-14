from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

#render homepage
class HomePage(TemplateView):
    template_name = "votingapp/home.html"