from django.contrib import admin
from .models import Election, Candidate, Voter, Vote

# Register your models here.

admin.site.site_header = "General Voting App"
admin.site.site_title = "General Voting App Admin Area"
admin.site.index_title = "Welcome to the General Voting App Admin Area"

# Include Election and Candiates Model to the admin area
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Voter)
admin.site.register(Vote)