from django.contrib import admin

from terraformus.core.models import Profile, Solution, LifeCycle, LifeCycleInput, LifeCycleWaste, \
    Strategy, StrategySolution, ExternalAsset

admin.site.register(Profile)

admin.site.register(Solution)
admin.site.register(ExternalAsset)
admin.site.register(LifeCycle)
admin.site.register(LifeCycleInput)
admin.site.register(LifeCycleWaste)
admin.site.register(Strategy)
admin.site.register(StrategySolution)
