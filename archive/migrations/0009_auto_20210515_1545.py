# Generated by Django 3.2.3 on 2021-05-15 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0008_auto_20210515_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movement',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='playerdetail',
            old_name='game_id',
            new_name='game',
        ),
    ]