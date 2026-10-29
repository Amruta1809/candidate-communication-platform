from django.contrib import admin
from .models import Candidate, Message, Template
admin.site.register([Candidate, Message, Template])
