from django.urls import path

from baimanush_backend.videos.api.v1 import views

urlpatterns = [
    path("", views.VideoListViewset.as_view({"get": "list"})),
    path("<str:slug>", views.VideoListViewset.as_view({"get": "retrieve"})),
    path("most-viewed/", views.VideoListViewset.as_view({"get": "most_viewed"})),
]
