from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Game, Comment, GameCollectionItem


class GameAdmin(SummernoteModelAdmin):
    summernote_fields = ('review',)
    list_filter = ('status', 'created_on')
    list_display = (
        'title',
        'status',
        'author',
        'genre',
        'platform_played',
        'developer',
        'created_on',
        )
    search_fields = ['title', 'developer']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'game', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')


"""Code taken and adapted from PP4_My_Meal_Planner by AliOKeeffe"""


class GameCollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'stage')


admin.site.register(Game, GameAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GameCollectionItem, GameCollectionAdmin)
