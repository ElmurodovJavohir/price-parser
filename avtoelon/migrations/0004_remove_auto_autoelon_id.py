# Generated by Django 3.2 on 2024-05-25 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avtoelon', '0003_autolink_auto_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auto',
            name='autoelon_id',
        ),
    ]