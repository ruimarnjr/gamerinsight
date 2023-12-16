from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, GameCollectionItem, Game

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

class GameForm(forms.ModelForm):
    """ Create Recipe Form """
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['review'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """
        Get recipe model, choose fields to display and add summernote widget
        """
        model = Game
        fields = [
            'title', 
            'featured_image',
            'review',
            'status',
        ]
        widgets = {
            'review': SummernoteWidget(),
        }
   