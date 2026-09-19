from django.contrib import admin

# Register your models here.
from .models import Experience, Achievement, Project

admin.site.register(Experience)
admin.site.register(Achievement)
admin.site.register(Project)