from django.contrib import admin

from staffapp.models import StaffList, ClientList, ActionList, CompletedActionList, PlanedActionList

admin.site.register(StaffList)
admin.site.register(ClientList)
admin.site.register(ActionList)
admin.site.register(CompletedActionList)
admin.site.register(PlanedActionList)
