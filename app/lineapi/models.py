from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user_id;

class Channels(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=255, blank=False, null=False)
    channel_name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.channel_id;
