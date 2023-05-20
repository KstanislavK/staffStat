from django.contrib import admin

from staffapp.models import StaffList, ClientList, ActionList, CompletedActionList, PlanedTaskList

admin.register(StaffList)
admin.register(ClientList)
admin.register(ActionList)
admin.register(CompletedActionList)
admin.register(PlanedTaskList)
