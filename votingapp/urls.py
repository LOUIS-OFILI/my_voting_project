from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import HomePage

urlpatterns = [
 path('', HomePage.as_view(), name="home"),
]