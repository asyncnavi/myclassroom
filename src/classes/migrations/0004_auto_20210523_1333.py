# Generated by Django 3.2.3 on 2021-05-23 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0003_auto_20210523_0443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='is_closed',
        ),
        migrations.AddField(
            model_name='classwork',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='code',
            field=models.CharField(default='c2e041a6', editable=False, max_length=8, unique=True),
        ),
        migrations.RemoveField(
            model_name='submission',
            name='student',
        ),
        migrations.AddField(
            model_name='submission',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='authentications.user'),
            preserve_default=False,
        ),
    ]
