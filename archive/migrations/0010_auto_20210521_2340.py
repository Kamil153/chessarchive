# Generated by Django 3.2.2 on 2021-05-21 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0009_auto_20210515_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='black_move',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='movement',
            name='white_move',
            field=models.CharField(max_length=9),
        ),
    ]
