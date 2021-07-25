from django.urls import path, include
from .views import VideoView, MovieView,  TagView, SeriesView, WatchlistView, UpdateWatchlistView, WatchlistStatusView
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter(trailing_slash =True)
router.register("videos", VideoView)
router.register("movies", MovieView)
router.register("series", SeriesView)
router.register("tags", TagView)
router.register("watchlist", WatchlistView)


urlpatterns = [
    path("", include(router.urls)),
    path("update-watchlist", UpdateWatchlistView.as_view()),
    path("check-watchlist", WatchlistStatusView.as_view()),

    # path("series-videos", VideoSeries.as_view()),
    # path("movie-videos/<int:blog_id>", SimilarVideos.as_view())
]
if settings.DEBUG:

    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)