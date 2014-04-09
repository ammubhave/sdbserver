from django.db import models


class Directory(models.Model):
    username = models.TextField()
    firstname = models.TextField()
    lastname = models.TextField()
    room = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    year = models.IntegerField(blank=True)
    cellphone = models.TextField(blank=True)
    email = models.TextField()