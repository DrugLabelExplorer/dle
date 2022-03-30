from django.contrib import admin

# Register your models here.
from .models import User, Tracking, Item

admin.site.register(Item)
admin.site.register(Tracking)
admin.site.register(User)
