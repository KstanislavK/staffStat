import calendar
from datetime import datetime

from django.db.models import Sum

from staffapp.models import CompletedActionList, PlanedActionList


def get_number_of_total_kpi(staff, month):
    _, num_days = calendar.monthrange(datetime.now().year, month)
    first_day = datetime(datetime.now().year, month, 1)
    last_day = datetime(datetime.now().year, month, num_days)
    completed_actions = CompletedActionList.objects.filter(manager=staff, date__gte=first_day, date__lte=last_day).aggregate(Sum('manager'))['manager__sum']
    planed_actions = PlanedActionList.objects.filter(staff=staff).aggregate(Sum('amount'))['amount__sum']
    if completed_actions is None:
        completed_actions = 0
    kpi = (completed_actions * 100) / planed_actions
    return kpi
