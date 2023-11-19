from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import UserProfile, Game, Review, Comment, AdminActivity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Game)
class GameAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

@admin.register(AdminActivity)
class AdminActivityAdmin(SummernoteModelAdmin):
    summernote_fields = ('activity_description',)
