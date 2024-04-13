from django.contrib import admin
from .models import Season, Show, CurrentlyWatching, UserEx
# Register your models here.
admin.site.register(Season)
admin.site.register(Show)
admin.site.register(CurrentlyWatching)
admin.site.register(UserEx)
