# Generated by Django 3.0.7 on 2020-07-14 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0002_disease'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='remedies',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='disease',
            name='treatments',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
