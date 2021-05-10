from django.db import models
from django.contrib.auth.models import User

COLORS = (
    ('black', 'black'),
    ('white', 'white')
)


class GameTime(models.Model):
    id = models.AutoField(primary_key=True)
    game_time = models.IntegerField()
    time_increment = models.IntegerField()

    def __str__(self):
        return str(self.game_time) + '+' + str(self.time_increment)


class ChessGame(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    game_time = models.ForeignKey(GameTime, on_delete=models.CASCADE, default=0)
    note = models.TextField()
    game_date = models.DateField()

    def __str__(self):
        return str(self.id)


class Movement(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(ChessGame, on_delete=models.CASCADE, default=0)
    move_nr = models.IntegerField()
    white_move = models.CharField(max_length=5)
    black_move = models.CharField(max_length=5)


class ChessPlayer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PlayerDetail(models.Model):
    id = models.AutoField(primary_key=True)
    rate = models.IntegerField()
    color = models.CharField(max_length=6, choices=COLORS, default='white')
    player = models.ForeignKey(ChessPlayer, on_delete=models.CASCADE, default=0)
    game_id = models.ForeignKey(ChessGame, on_delete=models.CASCADE, default=0)
