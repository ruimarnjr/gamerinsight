from django import forms
from .models import Comment, GameCollectionItem

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class GameCollectionForm(forms.ModelForm):
    """ Create GameCollection Form """
    
    class Meta:
        """Get game collection, choose fields to display"""
        model = GameCollectionItem
        fields = ('stage',)

   