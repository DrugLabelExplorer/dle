# Generated by Django 4.2 on 2023-05-02 04:35

from django.db import migrations, models
from django.db.models import F
from data.util import map_header_to_inverted_meta

def copy_field(apps, schema):
    ProductSection = apps.get_model('data', 'ProductSection')
    ProductSection.objects.all().update(agency_section_name=F('section_name'))

def update_section_names(apps, schema):
    ProductSection = apps.get_model('data', 'ProductSection')
    qs = ProductSection.objects.all()
    finished = 0
    for ps in qs.iterator():
        agency_section_name = ps.agency_section_name
        agency = ps.label_product.drug_label.source
        ps.section_name = map_header_to_inverted_meta(agency=agency, header=agency_section_name)
        ps.save()
        finished += 1
        if finished % 10000 == 0:
            print(f'Finished {finished} rows')


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_merge_20230421_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsection',
            name='original_section_name_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productsection',
            name='agency_section_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        # Copy to the new column
        migrations.RunPython(code=copy_field, reverse_code=migrations.RunPython.noop),
        # Now repopulate the existing section_name column
        migrations.RunPython(code=update_section_names, reverse_code=migrations.RunPython.noop)
    ]