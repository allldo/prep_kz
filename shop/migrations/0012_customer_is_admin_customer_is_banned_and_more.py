# Generated by Django 4.1.1 on 2022-10-25 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_address_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='total_messages',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
