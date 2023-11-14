from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import HomePage
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
 path('', HomePage.as_view(), name="home"),
 path('demo',TemplateView.as_view(template_name="bootstrap_base.html"),name='demo'),
path('popovers',TemplateView.as_view(template_name="bootstrap_popovers.html"), name="popovers"),
path('login',auth_views.LoginView.as_view(), name="login"),
]