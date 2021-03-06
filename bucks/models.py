from django.db import models
#imports for Point model
from django.db.models.signals import post_save
from django.contrib.auth.models import  User
#model related to a new user creation
class Point(models.Model):
    user             = models.ForeignKey(User, unique=None, on_delete=models.CASCADE, related_name="point", null=True)
    strava_connected = models.BooleanField(null=False, default=False)
    athlete_id       = models.CharField(max_length=100, null=True, blank=True, unique=True)
    miles            = models.DecimalField(decimal_places=1, max_digits=10000, null=True, blank=True, default=0)
    community        = models.DecimalField(decimal_places=1, max_digits=10000, null=True, blank=True, default=0)
    total            = models.DecimalField(decimal_places=1, max_digits=10000, null=True, blank=True, default=0)
    epoch            = models.CharField(max_length=100)
    refresh_token    = models.CharField(max_length=100)
    access_token     = models.CharField(max_length=100)
    community_code   = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.get_username()

class Admin_community_code(models.Model):
    generated_code   = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.generated_code

#allows the creation of the Point model whenever a new user is created. Stackoverflow FTW.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Point.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

# Major help from (ref: https://codingwithmitch.com/courses/building-a-website-django-python/blog-post-model-django/)
#imports for Blog model
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver
import datetime

#defines the upload loaction of any media uploaded
def upload_loaction(instance, filename, **kwargs):
    file_path = 'bucks/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
        )
    return file_path


class Post(models.Model):
    title       = models.CharField(max_length=50, null=False, blank=False)
    body        = models.TextField(max_length=5000, null=False, blank=False)
    image       = models.ImageField(upload_to=upload_loaction, null=False, blank=True)
    date_pub    = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_up     = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    slug        = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, *args, **kwargs):
    instance.image.delete(False)

def pre_save_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.title + "-" + str(datetime.datetime.now()))

pre_save.connect(pre_save_post_receiever, sender=Post)
