from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.crypto import get_random_string 
# Ticket code generation is implemented via get_random_string()

class Ticket(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=8)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class TicketPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    ticket_code = models.CharField(max_length=50, unique=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f'Ticket Purchase: {self.user.username} ({self.purchase_date})'

