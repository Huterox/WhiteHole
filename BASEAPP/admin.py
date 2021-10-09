from django.contrib import admin

# Register your models here.
from BASEAPP import models

admin.site.register(models.User)