# Generated by Django 5.1.5 on 2025-01-18 12:27

import django.db.models.deletion
import django_ckeditor_5.fields
import main.fields
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryLecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория лекции',
                'verbose_name_plural': 'Категории лекций',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CategoryNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория новости',
                'verbose_name_plural': 'Категории новостей',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CategoryProg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория програмы',
                'verbose_name_plural': 'Категории программ',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Раздел сайта')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Раздел сайта',
                'verbose_name_plural': 'Разделы сайта',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Prog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('photo', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Текст')),
                ('photo2', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото2')),
                ('selection_procedure', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Порядок отбора')),
                ('photo3', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото3')),
                ('selection_procedure2', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Порядок отбора 2 абзац')),
                ('photo4', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото4')),
                ('prog_statement', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Положение о программе')),
                ('photo5', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото5')),
                ('prog_statement2', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Положение о программе 2 абзац')),
                ('name_pdffile', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя PDF файла')),
                ('pdffile', models.FileField(blank=True, null=True, upload_to='pdf/%Y/%m/%d/', verbose_name='PDF')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('time_start', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время начала программы')),
                ('time_ending', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания программы')),
                ('is_published', models.BooleanField(verbose_name='Публикация')),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.categoryprog', verbose_name='Категория')),
                ('registration', models.ManyToManyField(blank=True, related_name='progs', to=settings.AUTH_USER_MODEL, verbose_name='Участники программы')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supervisor', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель')),
            ],
            options={
                'verbose_name': 'Программа',
                'verbose_name_plural': 'Программы',
                'ordering': ['time_create', 'title'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Текст')),
                ('photo', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='фото 633x550px')),
                ('content2', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Текст2')),
                ('photo2', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='фото2')),
                ('photo3', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото№3')),
                ('content3', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Текст3')),
                ('photo4', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото№4')),
                ('photo5', main.fields.WEBPField(blank=True, null=True, upload_to=main.models.image_folder, verbose_name='Фото№5')),
                ('content4', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Текст4')),
                ('time_create', models.DateTimeField(verbose_name='Дата и время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.categorynews', verbose_name='Категория')),
                ('prog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.prog', verbose_name='Программа')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['time_create', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('URL', models.URLField(blank=True, verbose_name='Ссылка на видео')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.categorylecture', verbose_name='Категория')),
                ('prog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.prog', verbose_name='Программа')),
            ],
            options={
                'verbose_name': 'Лекции',
                'verbose_name_plural': 'Лекции',
                'ordering': ['time_create', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Текст')),
                ('name_pdffile', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя PDF файла')),
                ('doc_file', models.FileField(blank=True, null=True, upload_to='pdf/%Y/%m/%d/', verbose_name='Файл')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('section', models.ManyToManyField(blank=True, related_name='Документы', to='main.section', verbose_name='Раздел сайта')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'ordering': ['time_create'],
            },
        ),
    ]
