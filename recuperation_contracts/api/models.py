from django.db import models

# Create your models here.

class Contracts(models.Model):
    
    issue_date = models.DateField()
    born_date = models.DateField()
    value = models.FloatField()
    cpf = models.CharField(max_length=11)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=2)
    city = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    tax = models.FloatField()


class Invoice(models.Model):
    contract = models.ForeignKey(Contracts,
                                 related_name='invoices',
                                 on_delete=models.CASCADE)
    invoice_number = models.IntegerField()
    value = models.FloatField()
    due_date = models.DateField()



