from django.urls import path

from baimanush_backend.articles.api.v1 import views

urlpatterns = [
    path(
        "members-only/<str:slug>",
        views.MemberPostDetailViewset.as_view({"get": "member_only_post"}),
    ),
    path("category-articles/<slug:category_slug>", views.PostListViewset.as_view({"get":"all_article_list_via_category"})),
    path(
        "category-post/<slug:category_slug>",
        views.PostListViewset.as_view({"get": "article_list_via_category"}),
    ),
    path(
        "post/<str:slug>", views.PostDetailViewset.as_view({"get": "retrieve_by_slug"})
    ),
    path(
        "home_content/", views.PostListViewset.as_view({"get": "home_screen_content"})
    ),
    path(
        "<str:category_slug>/<str:slug>",
        views.PostDetailViewset.as_view({"get": "retrieve"}),
    ),
    path(
        "members-only/", views.PostListViewset.as_view({"get": "is_member_only_posts"})
    ),
    path("trending-posts/", views.PostListViewset.as_view({"get": "trending_posts"})),
]
