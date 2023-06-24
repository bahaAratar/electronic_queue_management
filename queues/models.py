from django.db import models
from ticket.models import Ticket
from account.models import CustomUser

class Window(models.Model):
    operator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_works = models.BooleanField(default=False)

    def __str__(self):
        return f"№{self.id}, cвободен? {self.is_available}, работает? {self.is_works}"


class Queue(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    is_served = models.BooleanField(default=False)

    def __str__(self):
        return f"№{self.id}, билет: {self.ticket.number}, is_sedved = {self.is_served}"