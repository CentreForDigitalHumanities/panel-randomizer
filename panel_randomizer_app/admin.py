from django.contrib import admin

# Register your models here.

from .models import Participant
from .models import Survey

# admin.site.register(Participant)
#admin.site.register(Survey)

# eigen class voor de Survey om last_group niet te tonen
class SurveyAdmin(admin.ModelAdmin):
      exclude = ('last_group',)

admin.site.register(Survey, SurveyAdmin)