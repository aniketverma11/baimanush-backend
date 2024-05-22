from django.urls import path, include
from baimanush_backend.comments.api import views


urlpatterns = [
    path("article/<str:post_slug>", views.PostCommentsViewset.as_view({"post":"create"})),
    path("article-list/<str:post_slug>", views.PostCommentListViewset.as_view({"get": "list"})),
    path("photos/",views.PhotoCommentsViewset.as_view({"post":"create"})),
    path("photos-list/",views.PhotoCommentsListViewset.as_view({"get":"list"})),
    path("video/",views.CommentsViewset.as_view({"post":"create"})),
    path("video-list/",views.CommentsListViewset.as_view({"get":"list"}))
]