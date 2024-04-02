from django.contrib import admin
from .models import Season, Show, CurrentlyWatching, Watched
# Register your models here.
admin.site.register(Season)
admin.site.register(Show)
admin.site.register(CurrentlyWatching)
admin.site.register(Watched)
