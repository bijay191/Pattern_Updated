from django.contrib import admin
from .models import FileName, CentralizedPattern, GeneratedPattern

admin.site.register(FileName)
admin.site.register(CentralizedPattern)
admin.site.register(GeneratedPattern)