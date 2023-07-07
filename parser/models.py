from django.db import models

class Branches(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return {self.name}
