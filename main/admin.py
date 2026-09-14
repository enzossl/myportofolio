from django.contrib import admin

# Register your models here.
from .models import Experience, Achievement

admin.site.register("Experience")
admin.site.register("Achievement")