from django.contrib import admin

# Register your models here.

from .models import Participant
from .models import Survey

# class for Survey to omit last_group in admin
class SurveyAdmin(admin.ModelAdmin):
      exclude = ('last_group',)

admin.site.register(Survey, SurveyAdmin)