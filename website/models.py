from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField

STATUS = ((0, "Save for later"), (1, "Publish Now"))


class Game(models.Model):
    """Model representing a game."""
    title = models.CharField(max_length=255)
    featured_image = CloudinaryField('image', default='placeholder')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name="games", null=True, default='')
    review = SummernoteTextField(null=True, default='')
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=1)
    genre = models.CharField(max_length=100)
    platform_played = models.CharField(max_length=50)
    developer = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_on']

    """Code below taken and adapted from PP4_My_Meal_Planner by AliOKeeffe"""
    def get_absolute_url(self):
        """Return the URL for accessing the detail view of a game."""
        return reverse('game_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model representing a comment on a game."""
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='comments', default='')
    name = models.CharField(max_length=80, default='')
    email = models.EmailField(default='')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


"""Code below taken and adapted from PP4_My_Meal_Planner by AliOKeeffe"""


class GameCollectionItem(models.Model):
    """Model representing a comment on a game."""
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
