from django.db import models


# Section field name vs frontend display name
SEC_DISPLAY_NAMES = {
    'indication_usage': "Indication & Usage",
    'dosage': "Dosage & Administration",
    'contraindication': 'Contraindication',
    'adverse_reaction': 'Adverse Reaction',
    'description': 'Description'
}

class DrugLabel(models.Model):
    """Mock-up drug label data model
    """
    label_id = models.CharField(max_length=200)
    label_name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    indication_usage = models.TextField()
    dosage = models.TextField()
    contraindication = models.TextField()
    adverse_reaction = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"Label ID: {self.label_id}, Manufacturer: {self.manufacturer}"

