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
    approved = models.BooleanField(default=False)
    
    class Meta:
        """ To display the comments by created_on in ascending order """
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
