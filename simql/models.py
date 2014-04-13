from django.db import models


class Directory(models.Model):
    username = models.TextField()
    firstname = models.TextField()
    lastname = models.TextField()
    room = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    year = models.TextField(blank=True)
    cellphone = models.TextField(blank=True)
    homepage = models.TextField(blank=True)
    home_city = models.TextField(blank=True)
    home_state = models.TextField(blank=True)
    home_country = models.TextField(blank=True)
    quote = models.TextField(blank=True)
    favorite_category = models.TextField(blank=True)
    favorite_value = models.TextField(blank=True)
    private = models.BooleanField(default=False)
    email = models.TextField()
    title = models.TextField(blank=True)

    def __unicode__(self):
        return "{0} - {1} {2}".format(self.username, self.firstname, self.lastname)
