from datetime import datetime

from django.shortcuts import render, get_object_or_404

from staffapp.additional_funcs import get_number_of_total_kpi
from staffapp.models import StaffList, PlanedActionList


def index(request):
    staff = StaffList.objects.all()
    context = {
        'staff': staff
    }
    return render(request, 'staffapp/index.html', context)


def staff_details(request, pk):
    staff = get_object_or_404(StaffList, pk=pk)
    title = f'Карточка сотрудника {staff.name}'
    actions = PlanedActionList.objects.filter(staff=pk)
    total_kpi_current_month = get_number_of_total_kpi(pk, datetime.now().month)
    total_kpi_previous_month = get_number_of_total_kpi(pk, datetime.now().month - 1)
    context = {
        'staff': staff,
        'title': title,
        'actions': actions,
        'total_kpi_current_month': total_kpi_current_month,
        'total_kpi_previous_month': total_kpi_previous_month
    }
    return render(request, 'staffapp/staff.html', context)
