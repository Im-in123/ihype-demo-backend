from django.contrib import admin
from .models import  Video, Movie, Tag, Series, Season, Episode, Watchlist


admin.site.register(Video)
admin.site.register(Movie)
admin.site.register(Tag)
admin.site.register((Series, Season, Episode,))
admin.site.register(Watchlist)
