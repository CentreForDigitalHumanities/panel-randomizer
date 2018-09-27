from django.contrib import admin

# Register your models here.

from .models import Participant
from .models import Survey, SurveyGroup


class SurveyGroupInline(admin.TabularInline):
    help_text = "Lorem ipsum"
    fields = ('fill_count',)
    model = SurveyGroup
    verbose_name = ""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SurveyAdmin(admin.ModelAdmin):
    inlines = [SurveyGroupInline]
    exclude = ('last_group',)

    def save_model(self, request, obj, form, change):
        missing = list(range(1, obj.group_count + 1))
        # update the number of groups
        for group in SurveyGroup.objects.filter(survey=obj):
            if group.group_number > obj.group_count or \
                not group.group_number in missing:
                group.delete()
                # duplicate entry or number out of bounds
                continue

            if group.group_number in missing:
                missing.remove(group.group_number)

        for group_number in missing:
            SurveyGroup(survey=obj,
                group_number=group_number).save()

        super().save_model(request, obj, form, change)


admin.site.register(Survey, SurveyAdmin)
