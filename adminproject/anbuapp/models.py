from django.db import models
from django.contrib.auth.models import AbstractUser


# ============================================================
# CUSTOM USER
# ============================================================

class customuser(AbstractUser):

    email = models.EmailField(
        max_length=254,
        null=True
    )

    phone = models.IntegerField(
        null=True
    )

    address = models.CharField(
        max_length=50,
        null=True
    )


# ============================================================
# LOAN PREDICTION
# ============================================================

class LoanPrediction(models.Model):

    loan_id = models.IntegerField()

    no_of_dependents = models.IntegerField()

    education = models.CharField(
        max_length=50
    )

    self_employed = models.CharField(
        max_length=10
    )

    income_annum = models.FloatField()

    loan_amount = models.FloatField()

    loan_term = models.FloatField()

    cibil_score = models.FloatField()

    # Asset details
    # These are optional in the form.
    # Empty values are stored as 0.

    residential_assets_value = models.FloatField(
        default=0
    )

    commercial_assets_value = models.FloatField(
        default=0
    )

    luxury_assets_value = models.FloatField(
        default=0
    )

    bank_asset_value = models.FloatField(
        default=0
    )

    # Final prediction

    loan_status = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):

        return str(self.loan_id)