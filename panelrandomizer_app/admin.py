from django.contrib import admin

# Register your models here.

from .models import Participant
from .models import Survey

admin.site.register(Participant)
admin.site.register(Survey)
