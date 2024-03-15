from django.urls import path

from baimanush_backend.articles.api.v1 import views

urlpatterns = [
    path(
        "home_content/", views.PostListViewset.as_view({"get": "home_screen_content"})
    ),
    path(
        "<str:category_slug>/<str:slug>",
        views.PostDetailViewset.as_view({"get": "retrieve"}),
    ),
]
