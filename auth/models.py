from django.db import models
from simql.models import Directory


class UserPrivilege(models.Model):
    user = models.OneToOneField(Directory)
    privileges = models.TextField()  # a JSON encoded list of privileges


class App(models.Model):
    owner = models.ForeignKey(Directory)
    app_key = models.CharField(max_length=32)
    app_secret = models.CharField(max_length=32)
    default_privileges = models.TextField()
    extended_privileges = models.TextField()
    redirect_url = models.TextField()

    def __unicode__(self):
        return "{0} ({1})".format(self.app_key, self.owner)


class AccessToken(models.Model):
    access_token = models.CharField(max_length=32, unique=True)
    expires = models.DateTimeField()
    privileges = models.TextField()  # a JSON encoded list of permissions

    def __unicode__(self):
        return "{0}".format(self.access_token)
