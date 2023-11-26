from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import UserProfile, Game, Review, Comment, AdminActivity

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1

class GameAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('title', 'release_date', 'genre', 'platform', 'developer')
    search_fields = ['title', 'developer']
    inlines = [ReviewInline]

class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('user', 'game', 'rating', 'date_posted')
    search_fields = ['user__username', 'game__title']
    list_filter = ('rating', 'date_posted')
    inlines = [CommentInline]

class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('user', 'review', 'date_posted')
    search_fields = ['user__username', 'review__game__title']
    list_filter = ('date_posted',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

class AdminActivityAdmin(SummernoteModelAdmin):
    summernote_fields = ('activity_description',)
    list_display = ('user', 'activity_type', 'date_performed')
    search_fields = ['user__username', 'activity_type']
    list_filter = ('date_performed',)

admin.site.register(UserProfile)
admin.site.register(Game, GameAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AdminActivity, AdminActivityAdmin)