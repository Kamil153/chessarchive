# Generated by Django 3.2.2 on 2021-05-10 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessGames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('game_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ChessPlayers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GameTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_time', models.IntegerField()),
                ('time_increment', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_nr', models.IntegerField()),
                ('white_move', models.CharField(max_length=5)),
                ('black_move', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('color', models.CharField(choices=[('black', 'black'), ('white', 'white')], default='white', max_length=6)),
            ],
        ),
    ]
