# Generated by Django 5.1.5 on 2025-02-17 06:47

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_doc_file_documents_pdf_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Текст'),
        ),
    ]
