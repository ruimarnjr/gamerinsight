from django import forms
from .models import Comment, GameCollectionItem

class CommentForm(forms.ModelForm):
    """ Create Comment Form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        model = Comment
        fields = ('body',)


class GameCollectionForm(forms.ModelForm):
    """ Create GameCollection Form """
    
    class Meta:
        """Get game collection, choose fields to display"""
        model = GameCollectionItem
        fields = ('stage',)

   