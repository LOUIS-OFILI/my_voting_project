from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.

#render homepage
class HomePage(TemplateView):
    template_name = "votingapp/home.html"

    #render user dashboard

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "votingapp/user.html"