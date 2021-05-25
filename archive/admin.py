from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ChessGame)
class ChessGameAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'game_time', 'game_date']
    list_filter = ['user', 'game_time', 'game_date']


@admin.register(GameTime)
class GameTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_time', 'time_increment']
    list_filter = ['game_time']


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['id', 'game_id', 'move_nr', 'white_move', 'black_move']
    list_filter = ['game_id']


@admin.register(ChessPlayer)
class ChessPlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']


@admin.register(PlayerDetail)
class PlayerDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'rate', 'color', 'player', 'game_id']
    list_filter = ['player', 'game_id', 'rate']
