# Generated by Django 3.2.6 on 2021-10-04 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_bolg_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bolg',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
