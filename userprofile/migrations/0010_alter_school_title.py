# Generated by Django 5.1.5 on 2025-04-16 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_remove_school_address_remove_school_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='title',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Название'),
        ),
    ]
