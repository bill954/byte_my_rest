# Generated by Django 4.2 on 2023-06-01 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_rename_remainder_sended_order_reminder_sended'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='descritpion',
            new_name='description',
        ),
    ]
