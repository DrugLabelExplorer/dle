from django.db import models


class DrugLabel(models.Model):
    label_id = models.CharField(max_length=200)
    label_name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    indication_usage = models.TextField()
    dosage = models.TextField()
    contraindication = models.TextField()
    adverse_reaction = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"Label ID: {self.label_id}\nManufacturer: {self.manufacturer}"

