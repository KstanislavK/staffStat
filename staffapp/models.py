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


class ActionList(models.Model):
    """Действия сотрудника"""
    name = models.CharField(max_length=30)

    def get_number_of_completed_action(self):
        """сколько раз выполнено определенное действие"""
        amount = CompletedActionList.objects.filter(name=self.pk).annotate(action_sum=Sum('name'))['action_sum']
        return amount
    
    def get_planed_action_amount(self):
        amount = PlanedActionList.objects.get(name=self.pk).amount
        return amount


class CompletedActionList(models.Model):
    """Выполненные действия сотрудника"""
    name = models.ForeignKey(ActionList, on_delete=models.PROTECT)
    manager = models.ForeignKey(StaffList, on_delete=models.PROTECT)
    client = models.ForeignKey(ClientList, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)


class PlanedActionList(models.Model):
    """Установленный план на действия"""
    name = models.ForeignKey(ActionList, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()


