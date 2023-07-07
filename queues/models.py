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

    window = models.ForeignKey(Window, on_delete=models.CASCADE, null=True, blank=True)

    creation_date = models.DateTimeField(null=True, blank=True)
    service_start = models.DateTimeField(null=True, blank=True)
    service_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"№{self.id}, билет: {self.ticket.number}, is_sedved = {self.is_served}"
    
class Operathor(models.Model):
    operathor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True)
    client = models.ManyToManyField(Queue,blank=True)
    window = models.ForeignKey(Window, on_delete=models.CASCADE,blank=True)
    
    word_start = models.DateTimeField(null=True, blank=True)
    word_end = models.DateTimeField(null=True, blank=True)
