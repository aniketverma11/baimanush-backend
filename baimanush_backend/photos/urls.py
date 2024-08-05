from django.urls import path
from baimanush_backend.photos.api.v1 import views

urlpatterns = [
    path("", views.PhotosViewSet.as_view({"get": "list"})),
    path("<slug:slug>", views.PhotosViewSet.as_view({"get": "get"})),
    path("most-viewed/", views.PhotosViewSet.as_view({"get": "most_viewed"})),
    path("rss-feed/", views.PhotosViewSet.as_view({"get":"rss_feed_list"})),
]
