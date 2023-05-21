import calendar
from datetime import datetime

from django.db import models
from django.db.models import Sum


class StaffList(models.Model):
    """Данные сотрудника"""
    name = models.CharField(max_length=50)
    # photo = models.FileField
    city = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    appointments_date = models.DateField()
    effective_months = models.IntegerField(default=0)
    ineffective_months = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_clients(self):
        """все клиенты менеджера"""
        clients = ClientList.objects.filter(manager=self.pk)
        return clients


class ClientList(models.Model):
    """Данные клиента"""
    name = models.CharField(max_length=30)
    manager = models.ForeignKey(StaffList, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    address = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class ActionList(models.Model):
    """Действия сотрудника"""
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CompletedActionList(models.Model):
    """Выполненные действия сотрудника"""
    name = models.ForeignKey(ActionList, on_delete=models.PROTECT)
    manager = models.ForeignKey(StaffList, on_delete=models.PROTECT)
    client = models.ForeignKey(ClientList, on_delete=models.PROTECT)
    date = models.DateTimeField()

    def __str__(self):
        return self.name.name


class PlanedActionList(models.Model):
    """Установленный план на действия"""
    name = models.ForeignKey(ActionList, on_delete=models.PROTECT)
    staff = models.ForeignKey(StaffList, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name.name

    def get_number_of_completed_action_and_kpi(self):
        completed_amount = CompletedActionList.objects.filter(name=self.name, manager=self.staff).aggregate(Sum('manager'))['manager__sum']
        if completed_amount is None:
            completed_amount = 0
        plan_amount = self.amount
        kpi = (completed_amount * 100) / plan_amount
        context = {
            'completed_amount': completed_amount,
            'plan_amount': plan_amount,
            'kpi': kpi
        }
        return context

    def get_number_of_completed_action_and_kpi_prev_month(self):
        _, num_days = calendar.monthrange(datetime.now().year, datetime.now().month-1)
        first_day = datetime(datetime.now().year, datetime.now().month-1, 1)
        last_day = datetime(datetime.now().year, datetime.now().month-1, num_days)
        completed_amount = CompletedActionList.objects.filter(name=self.name, manager=self.staff, date__gte=first_day, date__lte=last_day).aggregate(Sum('manager'))['manager__sum']
        if completed_amount is None:
            completed_amount = 0
        plan_amount = self.amount
        kpi = (completed_amount * 100) / plan_amount
        context = {
            'completed_amount': completed_amount,
            'plan_amount': plan_amount,
            'kpi': kpi
        }
        return context


