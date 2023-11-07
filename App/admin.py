from django.contrib import admin
from .models import Property
from .models import Property_type,Notification

# Register your models here.
admin.site.register(Property)
admin.site.register(Property_type)
admin.site.register(Notification)
