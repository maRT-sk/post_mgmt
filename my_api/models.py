from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
