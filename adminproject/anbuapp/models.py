from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class customuser(AbstractUser):
    email=models.EmailField(max_length=254,null=True)
    phone=models.IntegerField(null=True)
    address=models.CharField(max_length=50,null=True)
    
class LoanPrediction(models.Model):
   
    loan_id = models.IntegerField()
    no_of_dependents = models.IntegerField()
    education = models.CharField(max_length=50)
    self_employed = models.CharField(max_length=10)
    income_annum = models.FloatField()
    loan_amount = models.FloatField()
    loan_term = models.FloatField()
    cibil_score = models.FloatField()
    residential_assets_value = models.FloatField()
    commercial_assets_value = models.FloatField()
    luxury_assets_value = models.FloatField()
    bank_asset_value = models.FloatField()
    loan_status = models.CharField(max_length=20, null=True, blank=True)