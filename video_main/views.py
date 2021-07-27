from .serializers import MovieSerializer,  TagSerializer, SeriesSerializer, VideoSerializer, WatchListSerializer
from rest_framework.viewsets import ModelViewSet
from .models import  Video, Movie, Tag, Series, Watchlist
from rest_framework.generics import ListAPIView
from django.db.models import Count, Q
from user_controller.models import CustomUser
from videosite.custom_methods import IsAuthenticatedCustom
from user_controller.views import decodeJWT

# from rest_framework.pagination import PageNumberPagination

# class PaginationInterfae(PageNumberPagination):
#     page_size =20

from random import shuffle
class MovieView(ModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticatedCustom,)
    # pagination_class = PaginationInterfae
    serializer_class = MovieSerializer
    lookup_field = "slug"

    # def get_queryset(self):
    #     my_list = list(self.queryset)
    #     shuffle(my_list) 
    #     return my_list



class TagView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class WatchlistView(ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = (IsAuthenticatedCustom,)


    def get_queryset(self):
        try:
            query = self.request.query_params.dict()
            keyword = query.get("keyword", None)
            user = decodeJWT(keyword)
            # user = CustomUser.objects.get(id= int(keyword))
            query_data = self.queryset.filter(user =user)
            return query_data
        except Exception as e:
            print("watchlist viewset::::",e)
            return None

class SeriesView(ModelViewSet):
    queryset = Series.objects.all()
    # pagination_class = PaginationInterfae
    serializer_class = SeriesSerializer
    # permission_classes = (IsAuthenticatedCustom,)
    lookup_field = "slug"

class VideoView(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticatedCustom,)

   

    def get_queryset(self):
        query = self.request.query_params.dict()
        keyword = query.get("keyword", None)
        query_data = self.queryset
        if keyword:
            query_data = query_data.filter(
                Q(title__icontains=keyword) |
                Q(title__iexact=keyword) |
                Q(movie__title__icontains=keyword) |
                Q(movie__title__iexact=keyword)  |
                Q(series__title__icontains=keyword) |
                Q(series__title__iexact=keyword)
            ).distinct()
        return query_data

from django.http import JsonResponse

class WatchlistStatusView(ListAPIView):
    permission_classes = (IsAuthenticatedCustom,)

    
    def post(self, request, *args, **kwargs):
        print("request.data::::", request.data)
        video_type = request.data.get("type")
        v_id = request.data.get("vid")
        user_id = request.data.get("user_id")
 
        if video_type=="movie":
            try:
                user  = CustomUser.objects.get(id = user_id)
                print("user:::::::",user)
                qs = Watchlist.objects.all().filter(user=user)[0]
                print("here1:::::",qs)
                # print(qs.__dict__)
                # print(dir(qs))
                print(qs.favorite_movie)
            except Exception as e:
                qs = Watchlist.objects.create(user=user)
                print("eeeee:::::",e)
                print(" but created watchlist", qs)
                
            try:
                qs1 = Movie.objects.get(id = v_id)
                print("here2:::::",qs1)
            except Exception as e:
                print("eeeeee::::", e)

            if video_type =="movie":
                qs2 = qs.favorite_movie.all()
                print("alll:::::",qs2)
                if qs1 in qs2:
                    print("Yeah its in favorites")
                    return JsonResponse({"data":"exist-true"})

                else:
                    print("its not in favorites")
                    return JsonResponse({"data":"exist-false"})

            
        elif video_type =="series":

            try:
                user  = CustomUser.objects.get(id = user_id)
                print("user:::::::",user)
                qs = Watchlist.objects.all().filter(user=user)[0]
                print("here1:::::",qs)
                # print(qs.__dict__)
                # print(dir(qs))
                print(qs.favorite_series)
            except Exception as e:
                qs = Watchlist.objects.create(user=user)
                print("eeeee:::::",e)
                print(" but created watchlist", qs)
                
            try:
                qs1 = Series.objects.get(id = v_id)
                print("here2:::::",qs1)
            except Exception as e:
                print("eeeeee::::", e)

            if video_type =="series":
                qs2 = qs.favorite_series.all()
                print("alll:::::",qs2)
                if qs1 in qs2:
                    print("Yeah its in favorites")
                    return JsonResponse({"data":"exist-true"})

                else:
                    print("its not in favorites")
                    return JsonResponse({"data":"exist-false"})

        return JsonResponse({"data":"none"})

    

class UpdateWatchlistView(ListAPIView):
    permission_classes = (IsAuthenticatedCustom,)

    # permission_classes = (IsAuthenticatedCustom,)
    # serializer_class = FavoriteSerializer

    def post(self, request, *args, **kwargs):
        print("request.data::::", request.data)
        video_type = request.data.get("type")
        v_id = request.data.get("vid")
        user_id = request.data.get("user_id")


        if video_type =="movie":
            try:
                qs = Watchlist.objects.get(user=user_id)
                print("here1:::::",qs)
                # print(qs.__dict__)
                # print(dir(qs))
                print(qs.favorite_movie)
            except Exception as e:
                qs = Watchlist.objects.create(user=user_id)
                print("eeeee:::::",e)
                print(" but created watchlist", qs)
                
            try:
                qs1 = Movie.objects.get(id = v_id)
                print("here2:::::",qs1)
            except Exception as e:
                print("eeeeee::::", e)

            if video_type =="movie":
                qs2 = qs.favorite_movie.all()
                print("alll:::::",qs2)
                if qs1 in qs2:
                    print("Yeah")
                    qs.favorite_movie.remove(qs1)
                    return JsonResponse({"data":"not-yah"})
                else:
                    qs.favorite_movie.add(qs1)

                    print("its not but adding")
                    qs3 = CustomUser.objects.get(id= user_id)
                    print("added::::",qs3)
                    return JsonResponse({"data":"yah"})


        elif video_type =="series":
            try:
                qs = Watchlist.objects.get(user=user_id)
                print("here1:::::",qs)
                # print(qs.__dict__)
                # print(dir(qs))
                print(qs.favorite_series)
            except Exception as e:
                qs = Watchlist.objects.create(user=user_id)
                print("eeeee:::::",e)
                print(" but created watchlist", qs)
                
            try:
                qs1 = Series.objects.get(id = v_id)
                print("here2:::::",qs1)
            except Exception as e:
                print("eeeeee::::", e)

            if video_type =="series":
                qs2 = qs.favorite_series.all()
                print("alll:::::",qs2)
                if qs1 in qs2:
                    print("Yeah")
                    qs.favorite_series.remove(qs1)
                    return JsonResponse({"data":"not-yah"})
                else:
                    qs.favorite_series.add(qs1)

                    print("its not but adding")
                    qs3 = CustomUser.objects.get(id= user_id)
                    print("added::::",qs3)
                    return JsonResponse({"data":"yah"})

        
        return JsonResponse({"data":"nothing"})

        # try:
        #     qs = Watchlist.objects.get(user=self.request.user)
        # except Exception as e:
        #     print(e)
        #     Watchlist.objects.create(user= self.request.user)
        
        # qs1  = qs_favorite_series

        # qs = Watchlist_favorite_series
        # qs = Watchlist.objects.get(user=self.request.user)
        # fav = qs.
        # try:
        #     favorite_user = CustomUser.objects.get(id=id)
        # except Exception:
        #     raise Exception("Favorite user does not exist")

        # try:
        #     fav = request.user.user_favorites
        # except Exception:
        #     fav = Favorite.objects.create(user_id=request.user.id)

        # favorite = fav.favorite.filter(id=favorite_user.id)
        # if favorite:
        #     fav.favorite.remove(favorite_user)
        #     return Response("removed")

        # fav.favorite.add(favorite_user)
        # return Response("added")
########################
    # permission_classes = (IsAuthenticatedCustom,)
    # serializer_class = FavoriteSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         favorite_user = CustomUser.objects.get(id=serializer.validated_data["favorite_id"])
    #     except Exception:
    #         raise Exception("Favorite user does not exist")

    #     try:
    #         fav = request.user.user_favorites
    #     except Exception:
    #         fav = Favorite.objects.create(user_id=request.user.id)

    #     favorite = fav.favorite.filter(id=favorite_user.id)
    #     if favorite:
    #         fav.favorite.remove(favorite_user)
    #         return Response("removed")

    #     fav.favorite.add(favorite_user)
    #     return Response("added")
