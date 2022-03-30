# Generated by Django 3.1.1 on 2020-12-06 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('druglabelexplorer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='uploaded_image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=19),
        ),
    ]
