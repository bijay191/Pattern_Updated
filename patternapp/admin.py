from django.contrib import admin
from .models import TableLog, GeneratedPattern, PatternLayoutMapping

admin.site.register(TableLog)
admin.site.register(GeneratedPattern)
admin.site.register(PatternLayoutMapping)