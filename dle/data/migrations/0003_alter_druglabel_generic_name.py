# Generated by Django 4.0.2 on 2023-03-16 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_alter_productsection_section_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='druglabel',
            name='generic_name',
            field=models.CharField(db_index=True, max_length=2048),
        ),
    ]