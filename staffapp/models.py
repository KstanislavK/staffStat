import calendar
from datetime import datetime

from django.db import models
from django.db.models import Sum


class StaffList(models.Model):
    """Данные сотрудника"""
    name = models.CharField(max_length=50, verbose_name='ФИО')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото')
    city = models.CharField(max_length=30, verbose_name='Город')
    position = models.CharField(max_length=30, verbose_name='Должность')
    appointments_date = models.DateField(verbose_name='Дата назначения')
    effective_months = models.IntegerField(default=0, verbose_name='Эффективные месяцы')
    ineffective_months = models.IntegerField(default=0, verbose_name='Неэффективные месяцы')

    def __str__(self):
        return self.name

    def get_clients(self):
        """все клиенты менеджера"""
        clients = ClientList.objects.filter(manager=self.pk)
        clients_amount = ClientList.objects.filter(manager=self.pk).aggregate(Sum('manager'))['manager__sum']
        context = {
            'clients': clients,
            'clients_amount': clients_amount
        }
        return context


class ClientList(models.Model):
    """Данные клиента"""
    name = models.CharField(max_length=30, verbose_name='ФИО')
    manager = models.ForeignKey(StaffList, on_delete=models.PROTECT, verbose_name='ФИО менеджера', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='Тел. номер', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    address = models.CharField(max_length=120, verbose_name='Адрес', blank=True)

    def __str__(self):
        return self.name


class ActionList(models.Model):
    """Действия сотрудника"""
    name = models.CharField(max_length=30, verbose_name='Название')

    def __str__(self):
        return self.name


class CompletedActionList(models.Model):
    """Выполненные действия сотрудника"""
    name = models.ForeignKey(ActionList, on_delete=models.PROTECT, verbose_name='Название')
    manager = models.ForeignKey(StaffList, on_delete=models.PROTECT, verbose_name='ФИО менеджера')
    client = models.ForeignKey(ClientList, on_delete=models.PROTECT, verbose_name='ФИО клиента')
    date = models.DateTimeField(verbose_name='Дата действия')

    def __str__(self):
        return self.name.name


class PlanedActionList(models.Model):
    """Установленный план на действия"""
    name = models.ForeignKey(ActionList, on_delete=models.PROTECT, verbose_name='Название')
    staff = models.ForeignKey(StaffList, on_delete=models.PROTECT, verbose_name='ФИО менеджера')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')

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


