from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Game, Comment, GameCollection

class GameAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_filter = ('status', 'created_on')
    list_display = ('title', 'status', 'release_date', 'genre', 'platform', 'developer', 'created_on')
    search_fields = ['title', 'developer']

class CommentAdmin(admin.ModelAdmin):
    """Allows admin to manage comments on recipes via the admin panel"""
    list_display = ('name', 'body', 'game', 'created_on', 'approved')
    list_filter = ('created_on', 'approved')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

class GameCollectionAdmin(admin.ModelAdmin):
    """Allows admin to manage user game collection via the admin panel"""
    list_display = ('user', 'game', 'status')

admin.site.register(Game, GameAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GameCollection, GameCollectionAdmin)
