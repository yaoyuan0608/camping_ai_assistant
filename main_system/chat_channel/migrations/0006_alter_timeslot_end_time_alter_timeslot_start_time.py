# Generated by Django 4.2 on 2023-04-25 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_channel', '0005_usermessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.DateField(),
        ),
    ]