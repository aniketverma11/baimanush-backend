from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import (
    viewsets,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.authtoken.models import Token

from .serializers import (
    UserSerializer,
    CreateUserProfileSerializer,
    LoginSerializer,
    LoginResponseSerializer,
    MyTokenObtainPairSerializer,
    ForgotPasswordResetSerializer,
    ForgotPasswordSerializer,
)
from utils.response import cached_response

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CreateProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CreateUserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateUserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return cached_response(
            request=request,
            status=status.HTTP_201_CREATED,
            response_status="success",
            message="your request is under verification please check your mail to move forward",
            data={},
            meta={},
        )


class LoginViewSet(viewsets.ModelViewSet):

    """
    This viewset is used for Login

    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return LoginSerializer
        return LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_object = User.objects.get(email=serializer.data["email"])
            if user_object.is_active == False:
                return cached_response(
                    request=request,
                    status=status.HTTP_400_BAD_REQUEST,
                    response_status="error",
                    message="Sorry your request is under verification now",
                    data={},
                    meta={},
                )

            refresh = MyTokenObtainPairSerializer.get_token(user_object)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            loginresponseserializer_objects = LoginResponseSerializer(
                {
                    "user_profile": user_object,
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                }
            )
        return cached_response(
            request=request,
            status=status.HTTP_201_CREATED,
            response_status="success",
            message="Login Successfully",
            data=loginresponseserializer_objects.data,
            meta={},
        )


class ForgotPasswordViewSet(viewsets.ModelViewSet):

    """
    This viewset is used for Login

    """

    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ForgotPasswordSerializer
        return ForgotPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="We have sent you an email to your email address {}".format(
                    serializer.data["email"]
                ),
                data={},
                meta={},
            )
        else:
            return cached_response(
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
                response_status="error",
                message="",
                data=serializer.errors,
                meta={},
            )


class ForgotPasswordResetViewSet(viewsets.ModelViewSet):

    """
    This viewset is used for Login

    """

    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordResetSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ForgotPasswordResetSerializer
        return ForgotPasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = ForgotPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data={},
                meta={},
            )
        else:
            return cached_response(
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
                response_status="error",
                message="",
                data=serializer.errors,
                meta={},
            )


class LogoutallViewSet(viewsets.ViewSet):

    """
    This viewset is used for Logout from all devices

    """

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        return cached_response(
            request=request,
            status=status.HTTP_201_CREATED,
            response_status="success",
            message="Logout Successfully",
            data={},
        )


class RefreshTokenView(TokenRefreshView):
    pass


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
