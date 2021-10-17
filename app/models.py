from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
# Create your models here.

SUBJECT_CHOICES = (
    ('Not Applicable', 'Not Applicable'),
    ('Math','Math'),
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('English', 'English'),
    ('Biology', 'Biology'),
    ('Physical Education','Physical Education'),
    ('Business', 'Business'),
    ('Economics', 'Economics')
)

UNI_CHOICES = (
    ('KFUPM', 'KFUPM'),
    ('Harvard', 'Harvard')
)

TYPE_CHOICES = (
    ('Question', 'Question'),
    ('Content Share', 'Content Share'),
    ('Rant', 'Rant')
)

LEVEL_CHOICES = (
    ("Preparatory", "Preparatory"),
    ("Freshman", "Freshman"),
    ("Sophomore","Sophomore"),
    ("Junior", "Junior"),
    ("Senior", "Senior")
)

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    uni = models.CharField(max_length=64, blank=True)
    profile_pic = models.ImageField(upload_to="profile/image/", null = True, blank = True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=64, choices=TYPE_CHOICES, blank=False, default="question")
    title = models.CharField(max_length=256)
    desc = models.TextField(max_length=2000)
    doc = models.FileField(upload_to="posts/doc/", blank=True, default = "null")
    video = models.CharField(max_length=1000, blank=True, default="")
    university = models.CharField(max_length=64, choices=UNI_CHOICES, default="other")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default= 0)
    comments = models.IntegerField(default= 0)
    subject = models.CharField(max_length=64, choices=SUBJECT_CHOICES, default="other")
    level = models.CharField(max_length=64, choices=LEVEL_CHOICES, default="Freshman")
    def filename(self):
        return os.path.basename(self.file.name)

class Likes(models.Model):
    user = models.CharField(max_length=256)
    post_number = models.IntegerField()

class Follow(models.Model):
    follower = models.CharField(max_length = 256)
    following = models.CharField(max_length = 256)

class Comments(models.Model):
    username = models.CharField(max_length=256)
    pic = models.CharField(max_length=256)
    post = models.IntegerField()
    content = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)


