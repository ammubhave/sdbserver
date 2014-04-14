from django.contrib import admin
from auth.models import App, AccessToken, UserPrivilege

# Register your models here.
admin.site.register(App)
admin.site.register(AccessToken)
admin.site.register(UserPrivilege)
