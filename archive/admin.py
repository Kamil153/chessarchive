from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ChessGame)
class ChessGameAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'game_time', 'game_date']


@admin.register(GameTime)
class GameTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_time', 'time_increment']


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_id', 'move_nr', 'white_move', 'black_move']


@admin.register(ChessPlayer)
class ChessPlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(PlayerDetail)
class PlayerDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'rate', 'color', 'player', 'game_id']
