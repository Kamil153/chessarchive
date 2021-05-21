from django.db import models
from django.contrib.auth.models import User

COLORS = (
    ('black', 'black'),
    ('white', 'white')
)


class GameTime(models.Model):
    game_time = models.IntegerField()
    time_increment = models.IntegerField()

    def __str__(self):
        return str(self.game_time) + '+' + str(self.time_increment)


class ChessGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    game_time = models.ForeignKey(GameTime, on_delete=models.CASCADE, default=0)
    note = models.TextField()
    game_date = models.DateField()


class Movement(models.Model):
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE, default=0)
    move_nr = models.IntegerField()
    white_move = models.CharField(max_length=5)
    black_move = models.CharField(max_length=5)


class ChessPlayer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PlayerDetail(models.Model):
    rate = models.IntegerField()
    color = models.CharField(max_length=6, choices=COLORS, default='white')
    player = models.ForeignKey(ChessPlayer, on_delete=models.CASCADE, default=0)
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE, default=0)
