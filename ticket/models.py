import random
import string
from django.db import models
from account.models import CustomUser
from django.utils import timezone


class Region(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

class Area(models.Model):
    title = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class City(models.Model):
    title = models.CharField(max_length=50, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Department(models.Model):
    title = models.CharField(max_length=50, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Ticket(models.Model):

    transaction_list = [('money_transfers', 'Money transfers'), ('bank_cards','Bank cards'), ('account_maintenance','Account maintenance')]
    status_list = [('not_active', 'Not active'), ('active', 'Active')]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE) # область
    area = models.ForeignKey(Area, on_delete=models.CASCADE) # район
    city = models.ForeignKey(City, on_delete=models.CASCADE) # город
    department = models.ForeignKey(Department, on_delete=models.CASCADE) #отделение

    transaction = models.CharField(choices=transaction_list, default='money_transfers', max_length=50)
    
    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(choices=status_list, default='not_active', max_length=50, blank=True)
    
    number = models.CharField(max_length=6, unique=True, blank=True)
    activation_code = models.CharField(max_length=7, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.activation_code:
            random_digits = ''.join(random.choices(string.digits, k=5))
            city_first_letter = self.department.city.title[0]
            department_first_letter = self.department.title[0]
            activation_code = f'{city_first_letter}{department_first_letter}{random_digits}'

            self.activation_code = activation_code

        if not self.number:
            transaction_code = self.transaction[0].upper()
            last_ticket_number = Ticket.objects.order_by('-id').first()
            if last_ticket_number:
                last_number = int(last_ticket_number.number[2:])
            else:
                last_number = -1
            new_number = f'{transaction_code}{str(last_number + 1).zfill(3)}'
            self.number = new_number

        super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id}, Билет: {self.number}, Владелец: {self.owner}, Операция: {self.transaction}, status {self.status}"