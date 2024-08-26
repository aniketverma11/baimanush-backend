from django.urls import path

from rest_framework_simplejwt.views import TokenBlacklistView

from baimanush_backend.users.api.views import (
    LoginViewSet,
    CreateProfileViewSet,
    RefreshTokenView,
    ForgotPasswordViewSet,
    ForgotPasswordResetViewSet,
    UserV2Viewset
)


from baimanush_backend.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path(
        "login/",
        LoginViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "signup/",
        CreateProfileViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "update-profile/", 
        UserV2Viewset.as_view(
            {
                "post": "sign_up",
            }
        ),
    ),
    path(
        "get-user/",
        UserV2Viewset.as_view(
            {
                "get": "get",
            }
        ),
    ),
    path(
        "forgot/",
        ForgotPasswordViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "forgot_reset/",
        ForgotPasswordResetViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "forgot_reset/",
        ForgotPasswordResetViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
