from django.contrib import admin
from .models import Election, Candidate, Vote, Position

admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Position)