from django.contrib import admin

from terraformus.core.models import Profile, Solution, SolutionType, SolutionPopulationTarget, SolutionDimensionTarget, \
    SolutionUNTarget, SolutionSector, WorkingExample, Reference, Document, LifeCycle, LifeCycleInput, LifeCycleWaste, \
    Strategy, StrategySolution

admin.site.register(Profile)

admin.site.register(Solution)
admin.site.register(SolutionType)
admin.site.register(SolutionPopulationTarget)
admin.site.register(SolutionDimensionTarget)
admin.site.register(SolutionUNTarget)
admin.site.register(SolutionSector)
admin.site.register(WorkingExample)
admin.site.register(Reference)
admin.site.register(Document)
admin.site.register(LifeCycle)
admin.site.register(LifeCycleInput)
admin.site.register(LifeCycleWaste)

admin.site.register(Strategy)
admin.site.register(StrategySolution)
