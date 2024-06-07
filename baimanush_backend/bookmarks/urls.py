from django.urls import path

from baimanush_backend.bookmarks.api.views import BookmarksViewSet


urlpatterns = [
    path("create/", BookmarksViewSet.as_view({"post":"create"})),
    path("list/", BookmarksViewSet.as_view({"get":"list"})),
    path("update/", BookmarksViewSet.as_view({"patch":"update"})),
]
