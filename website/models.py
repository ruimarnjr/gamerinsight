from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('avatar', default='avatar/default_avatar.png')

    def __str__(self):
        return self.user.username

class Game(models.Model):
    title = models.CharField(max_length=255)
    featured_image = CloudinaryField('image', default='placeholder')
    description = SummernoteTextField()  
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)
    developer = models.CharField(max_length=255)
    

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = SummernoteTextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  default=1)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.review.game.title}"

class AdminActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    activity_description = SummernoteTextField() 
    date_performed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
