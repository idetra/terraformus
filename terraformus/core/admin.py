from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from terraformus.core.models import  HomePageControl, Profile, Solution, LifeCycle, LifeCycleInput, LifeCycleWaste, \
    Strategy, StrategySolution, ExternalAsset, User


class HomePageControlAdmin(admin.ModelAdmin):

    def reminder(self, obj):
        return format_html("<strong>Don't forget to use embed link for video urls</strong>")

    reminder.short_description = 'Reminder'

    # This adds the 'reminder' field to the list display
    list_display = ('home_title', 'home_subtitle', 'active', 'reminder')


# Register your models here.
admin.site.register(HomePageControl, HomePageControlAdmin)
admin.site.register(Profile)
admin.site.register(Solution)
admin.site.register(ExternalAsset)
admin.site.register(LifeCycle)
admin.site.register(LifeCycleInput)
admin.site.register(LifeCycleWaste)
admin.site.register(Strategy)
admin.site.register(StrategySolution)
admin.site.register(User, UserAdmin)
