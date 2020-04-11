from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.CrashFile)
admin.site.register(models.Task)
admin.site.register(models.Developer)
admin.site.register(models.Department)
admin.site.register(models.WorkSpeed)
