# Generated by Django 4.2 on 2023-05-14 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userdocumentation_is_distinguished'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdocumentation',
            name='is_distinguished',
        ),
    ]
