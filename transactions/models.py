from django.db import models
from django.contrib.auth.models import User

class Transactions(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('salary', 'Salary'),
        ('rent', 'Rent'),
        ('shopping', 'Shopping'),
        ('healthcare', 'Healthcare'),
        ('bills', 'Bills'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=30, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    added_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount}"
