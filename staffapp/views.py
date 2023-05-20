from django.shortcuts import render, get_object_or_404

from staffapp.models import StaffList, CompletedActionList, ActionList, ClientList


def index(request):
    staff = StaffList.objects.all()
    context = {
        'staff': staff
    }
    return render(request, 'staffapp/index.html', context)


def staff_details(request, pk):
    staff = get_object_or_404(StaffList, pk=pk)
    title = f'Карточка сотрудника {staff.name}'
    actions = ActionList.objects.all()
    context = {
        'staff': staff,
        'title': title,
        'actions': actions
    }
    return render(request, 'staffapp/staff.html', context)
