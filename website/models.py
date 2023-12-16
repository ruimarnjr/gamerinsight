from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField

STATUS = ((0, "Save for later"), (1, "Publish Now"))

class Game(models.Model):
    title = models.CharField(max_length=255)
    featured_image = CloudinaryField('image', default='placeholder')
    description = SummernoteTextField()
    created_on = models.DateTimeField(auto_now=True)  
    release_date = models.DateField()
    status = models.IntegerField(choices=STATUS, default=1)
    genre = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)
    developer = models.CharField(max_length=255)

    class Meta:
        """To display the recipes by created_on in descending order"""
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    """Model for Comment"""
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='comments', default='')
    name = models.CharField(max_length=80, default='')
    email = models.EmailField(default='')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        """ To display the comments by created_on in ascending order """
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class GameCollectionItem(models.Model):
    """Model for Game Collection"""
    STAGE_CHOICES = [
        (0, "Playing"),
        (1, "Queued"),
        (2, "Completed "),
        (3, "Interested"),
        (4, "Abandoned"),        
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="game_collection")
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="game_collection_item")
    stage = models.IntegerField(choices=STAGE_CHOICES, default='0')

    class Meta:
        """To display the Game Collection Item by stage in ascending order"""
        ordering = ['stage']

    def __str__(self):
        return f"Current Stage {self.stage} by {self.user}"

    