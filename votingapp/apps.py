# this file is to define the apps configurations and behaviour of the application

from django.apps import AppConfig


class VotingappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'votingapp'
