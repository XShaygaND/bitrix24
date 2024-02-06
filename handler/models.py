from django.db import models


class Deal(models.Model):
    """Simple model with the required fields provided by bitrix24"""

    full_name = models.CharField(max_length=99)
    phone_number = models.CharField(max_length=99)
    comment = models.TextField(max_length=399, blank=True, null=True)
