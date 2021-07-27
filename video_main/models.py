from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

VIDEO_TYPE = (
    ('Series', 'Series'),
    ('Movie', 'Movie')
) 
class Tag(models.Model):
    title = models.CharField(max_length= 50, unique=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return  f"{self.title} Tag"

# class Video(models.Model):
#     # movie = models.ManyToManyField("Movie", related_name="video_movies", blank=True)
#     # series = models.ManyToManyField("Series", related_name="video_series", blank=True)
#     movie = models.ForeignKey("Movie", related_name="video_movies", blank=True, null=True, on_delete= models.CASCADE)
#     series = models.ForeignKey("Series", related_name="video_series", blank=True,  null=True, on_delete= models.CASCADE)
#     title = models.CharField(max_length= 255, null=True, blank=True)
#     videotype= models.CharField(choices= VIDEO_TYPE, max_length=11)

#     def __str__(self):
#         return  f"Video Type:{self.videotype}"

class Video(models.Model):
    movie = models.ManyToManyField("Movie", related_name="second_video_movies", blank=True)
    series = models.ManyToManyField("Series", related_name="second_video_series", blank=True)
    # movie = models.ForeignKey("Movie", related_name="video_movies", blank=True, null=True, on_delete= models.CASCADE)
    # series = models.ForeignKey("Series", related_name="video_series", blank=True,  null=True, on_delete= models.CASCADE)
    title = models.CharField(max_length= 255, blank=True)
    # slug= models.SlugField(default = "", editable = False, max_length=255)
    videotype= models.CharField(choices= VIDEO_TYPE, max_length=11)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return  f"Video Type: {self.videotype} {self.title}"       

class Movie(models.Model):

    # def get_tag():
    #     try:
    #         t  = Tag.objects.get(title = "Recommended")
    #     except:
    #         t = Tag.objects.create(title="Recommended")
    #     return str(t)
    author = models.ForeignKey("user_controller.CustomUser", related_name="movie_author", on_delete= models.CASCADE)
    title = models.CharField(max_length= 255, unique=True)
    slug= models.SlugField(default = "", editable = False, max_length=255)
    cover = models.ImageField( upload_to="movie_covers", default='default.jpg',)
    background_big_screen = models.ImageField(upload_to="movie_background_covers_bigscreen",default='default.jpg')
    background_small_screen = models.ImageField(upload_to="movie_background_covers_smallscreen",default='default.jpg')
    video = models.FileField(upload_to='movies_uploaded',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    trailer= models.FileField(upload_to='movie_trailer',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    subtitle_file = models.FileField(upload_to="movie_subtitles", null = True, blank= True)
    subtitle = models.CharField(max_length= 255, null=True, blank=True)
    description = models.CharField(max_length= 700, null=True, blank=True)
    # tags = models.ManyToManyField(Tag, related_name="movie_tags", default=get_tag())
    tags = models.ManyToManyField(Tag, related_name="movie_tags", blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    core_type= models.CharField(choices= VIDEO_TYPE, max_length=11)


    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return  f"{self.author.username} - {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode =True)
        super().save(*args, **kwargs)


class Series(models.Model):
    author = models.ForeignKey("user_controller.CustomUser", related_name="series_author", on_delete= models.CASCADE)
    title = models.CharField(max_length= 255, unique=True)
    slug= models.SlugField(default = "", editable = False, max_length=255)
    tags = models.ManyToManyField(Tag, related_name="series_tags", blank=True)
    season= models.ManyToManyField("Season", related_name="series_seasons", blank=True)
    cover = models.ImageField( upload_to="series_covers", default='default.jpg',)
    background_big_screen = models.ImageField(upload_to="series_background_covers_bigscreen",default='default.jpg')
    background_small_screen = models.ImageField(upload_to="series_background_covers_smallscreen",default='default.jpg')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    subtitle = models.CharField(max_length= 255, null=True, blank=True)
    description = models.CharField(max_length= 700, null=True, blank=True)
    trailer= models.FileField(upload_to='series_trailer',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    core_type= models.CharField(choices= VIDEO_TYPE, max_length=11)


    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return  f"{self.author.username} - {self.title}"


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode =True)
        super().save(*args, **kwargs)

class Season(models.Model):
    title = models.CharField(max_length= 255)
    series = models.ForeignKey("Series", related_name="series_link", on_delete= models.CASCADE, default="")
    season_num= models.IntegerField()
    episodes= models.ManyToManyField("Episode", related_name="series_episodes", blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return  f"{self.series.title} - Season {self.season_num}"



class Episode(models.Model):
    title = models.CharField(max_length= 255, default="episode")
    episode_num = models.IntegerField(default = 1)
    season = models.ForeignKey("Season", related_name="season_link", on_delete= models.CASCADE, default="")
    season_num = models.IntegerField(default = 1)
    cover = models.ImageField( upload_to="episode_covers", default='default.jpg')
    video = models.FileField(upload_to='episodes_uploaded',null=True, blank=True, \
                 validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    subtitle_file = models.FileField(upload_to="episode_subtitles", null = True, blank= True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # video_subtitle
    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return  f"{self.season} - {self.season} {self.title}"

class Watchlist(models.Model):
    user = models.OneToOneField("user_controller.CustomUser", related_name="user_favorites", on_delete=models.CASCADE)
    favorite_movie = models.ManyToManyField(Movie, related_name="user_series_watchlist" ,  blank=True)
    favorite_series = models.ManyToManyField(Series, related_name="user_series_watchlist",   blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Watchlist"

    class Meta:
        ordering = ("created_at",)















