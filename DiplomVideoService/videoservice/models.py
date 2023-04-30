from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class VSUser(models.Model):
    user_data = models.ForeignKey(User, on_delete=models.CASCADE)
    video_counter = models.IntegerField(default=0)
    like_counter = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    comment_counter = models.IntegerField(default=0)
    subscribers = models.ManyToManyField('VSUser', through='UserToUserSubscribe')

    def like(self):
        self.like_counter += 1
        self.save()

    def addedVideo(self):
        self.video_counter += 1
        self.save()

    def addedComment(self):
        self.comment_counter += 1
        self.save()

    def __str__(self):
        return f'{self.user_data.username}/ {self.video_counter} videos/ {self.like_counter} likes/ {self.comment_counter} comments.'


class VSVideo(models.Model):
    author = models.ForeignKey(VSUser, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    viewing = models.IntegerField(default=0)
    posted_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    comment_counter = models.IntegerField(default=0)

    def like(self):
        self.likes += 1
        self.author.like()
        self.save()

    def newViewing(self):
        self.viewing = self.viewing + 1
        self.save()

    def __str__(self):
        return f'{self.author.user_data.username}/ {self.viewing} viewing/ {self.likes} likes/ {self.comment_counter} comments/ posted - {self.posted_date}'


class VSComment(models.Model):
    author = models.ForeignKey(VSUser, on_delete=models.CASCADE)
    commented_video = models.ForeignKey(VSVideo, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    text = models.TextField(max_length=255)
    posted_date = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.likes = self.likes + 1
        self.author.like()
        self.save()

    def __str__(self):
        return f'from {self.author.user_data.username}/ {self.posted_date}/ {self.text}/ {self.likes} likes'


class UserToUserSubscribe(models.Model):
    subscribe_to_user = models.ForeignKey(VSUser, on_delete=models.CASCADE)
    subscribes_user = models.ForeignKey(VSUser, on_delete=models.CASCADE)
