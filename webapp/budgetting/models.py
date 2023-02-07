from django.db import models

class DailySpent(models.Model):
    spent_date = models.DateField()
    spent_amount = models.FloatField()
    spent_name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.spent_name} on {self.spent_date}: ${self.spent_amount}"

class DailyPaid(models.Model):
    paid_date = models.DateField()
    paid_amount = models.FloatField()
    def __str__(self):
        return f"{self.paid_date}: ${self.paid_amount}"

class Debt(models.Model):
    debt_name = models.CharField(max_length=64)
    debt_type = models.CharField(max_length=64)
    debt_amount = models.FloatField()
    def __str__(self):
        return f"{self.debt_name} - {self.debt_type} debt: ${self.debt_amount}"