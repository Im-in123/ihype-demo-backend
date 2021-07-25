from rest_framework import serializers
from .models import Video, Movie, Tag, Series, Season, Episode, Watchlist
from user_controller.serializers import CustomUserSerializer

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ("title",)



class MovieSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only = True)
    tags = TagSerializer(many=True)
    # comment_count= serializers.SerializerMethodField("get_comment_count")

    class Meta:
        model = Movie
        fields = "__all__"

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields ="__all__"

class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True)
    class Meta:
        model = Season
        fields ="__all__"

class SeriesSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only = True)
    season = SeasonSerializer(many=True)
    tags = TagSerializer(many=True)

    # comment_count= serializers.SerializerMethodField("get_comment_count")

    class Meta:
        model = Series
        fields = "__all__" 


# class VideoSerializer(serializers.ModelSerializer):
#     # movie = MovieSerializer
#     # series = SeriesSerializer
#     movie = MovieSerializer
#     series = SeriesSerializer
#     movie_id = serializers.IntegerField(write_only = True)
#     series_id = serializers.IntegerField(write_only = True)


#     class Meta:
#         model = Video
#         fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=True)
    series = SeriesSerializer(many=True)
    movie_id = serializers.IntegerField(write_only = True)
    series_id = serializers.IntegerField(write_only = True)


    class Meta:
        model = Video
        fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    favorite_movie = MovieSerializer(many=True)
   # # favorite_movie_id = serializers.IntegerField()
    favorite_series = SeriesSerializer(many=True)
   # # favorite_series_id = serializers.IntegerField()

    class Meta:
        model = Watchlist
        fields = "__all__"

