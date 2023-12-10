from .models import Comment, GameCollection
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class GameCollectionForm(forms.ModelForm):
    """ Create GameCollection Form """
    class Meta:
        """Get game collection, choose fields to display"""
        model = GameCollection
        fields = ('status',)