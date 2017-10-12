
from django.contrib import admin
from . import models

admin.site.register(models.Server)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.Memory)
admin.site.register(models.ServerRecord)