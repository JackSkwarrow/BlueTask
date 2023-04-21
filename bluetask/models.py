from django.db import models

# Create your models here.

class System(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True)
    support_group = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'system'


class SystemContract(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    amount_period = models.CharField(max_length=5)
    amount_type = models.CharField(max_length=5)
    authorization_percent = models.DecimalField(max_digits=19, decimal_places=2)
    from_date = models.DateField()
    order_number = models.CharField(max_length=12)
    request = models.CharField(max_length=12)
    to_date = models.DateField()
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    def __str__(self):
        return self.request + ' - ' + self.system.name

    class Meta:
        db_table = 'system_contract'
        unique_together = (('request', 'system'),)