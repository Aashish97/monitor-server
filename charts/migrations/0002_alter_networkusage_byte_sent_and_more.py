# Generated by Django 4.2.3 on 2023-07-20 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkusage',
            name='byte_sent',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='networkusage',
            name='bytes_received',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='networkusage',
            name='packet_received',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='networkusage',
            name='packet_sent',
            field=models.BigIntegerField(),
        ),
    ]