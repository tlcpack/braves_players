from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Player(models.Model): 
    """Model representing player"""

    # name of player
    name = models.CharField(max_length=250, help_text="Enter player's name")

    # stats for player
    stats = models.TextField(max_length=1000, help_text="Enter player's stats")

    # adding a slug
    slug = models.SlugField(unique=True, null=True, blank=True)

    # saving with slug
    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        if self.slug:
            return
        base_slug = slugify(self.name)
        slug = base_slug
        n = 0
        while Player.objects.filter(slug=slug).count():
            n +=1 
            slug = base_slug + "-" + str(n)
        self.slug = slug
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("player-detail", args=[str(self.id)])
    

class Comment(models.Model):

    # author posting a comment. one to many
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)

    #text of comment
    content = models.TextField(max_length=500)

    # date and time of post
    comment_date_added = models.DateTimeField(auto_now_add=True)

    # tying to player
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name="comments")

    # favorites
    favorited_by = models.ManyToManyField(User, related_name="favorite_comments")

    class Meta:
        ordering = ['comment_date_added']

    def __str__(self):
        return self.content