# Generated by Django 3.2.3 on 2021-05-21 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(default='32e69e80', editable=False, max_length=8, unique=True)),
                ('created', models.DateField(auto_now=True)),
                ('subject', models.CharField(max_length=200)),
                ('students', models.ManyToManyField(blank=True, related_name='students', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=100)),
                ('detail', models.TextField(blank=True, max_length=1000)),
                ('attached_file', models.FileField(blank=True, upload_to='classwork')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='submission')),
                ('is_submitted', models.BooleanField(default=False)),
                ('classwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classwork')),
                ('student', models.ManyToManyField(blank=True, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('annoucement', 'announcement'), ('studymaterial', 'studymaterial')], max_length=30)),
                ('detail', models.TextField(blank=True, max_length=1000)),
                ('attached_file', models.FileField(blank=True, upload_to='post')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classroom')),
            ],
        ),
    ]
