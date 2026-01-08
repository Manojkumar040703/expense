from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('NetBanking', 'Net Banking'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Cash')
    merchant_name = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    date = models.DateField()
    note = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f"{self.month}/{self.year} - ₹{self.amount}"
