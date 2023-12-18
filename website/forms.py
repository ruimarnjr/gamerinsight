from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, GameCollectionItem, Game


class CommentForm(forms.ModelForm):
    """Code taken from PP4_My_Meal_Planner by AliOKeeffe"""
    """ Create Comment Form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        model = Comment
        fields = ('body',)


class GameCollectionForm(forms.ModelForm):
    """Code taken and adapted from PP4_My_Meal_Planner by AliOKeeffe"""
    """ Create GameCollection Form """

    class Meta:
        """Get game collection, choose fields to display"""
        model = GameCollectionItem
        fields = ('stage',)


"""Code taken and adapted from PP4_My_Meal_Planner by AliOKeeffe"""


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['review'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        model = Game
        fields = [
            'title',
            'featured_image',
            'genre',
            'platform_played',
            'developer',
            'review',
        ]
        widgets = {
            'review': SummernoteWidget(),
        }
