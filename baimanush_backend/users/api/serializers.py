from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

from baimanush_backend.users.models import User as UserType
from utils.utils import (
    get_set_password_subject_message,
    get_subscription_request_subject_message,
)
from utils.utils import string_encrypt, decrypt_string



User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class CreateUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(mobile=data["phone_number"]).exists():
            raise serializers.ValidationError(
                "User with this mobile number  already exists"
            )
        if User.objects.filter(email=data["email"].lower()).exists():
            raise serializers.ValidationError(
                "User with this email {} already exists".format(data["email"])
            )

        return data

    def create(self, validated_data):
        user_object = User.objects.create_user(
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            name=validated_data["first_name"] + validated_data["last_name"],
            email=validated_data["email"],
            mobile=validated_data["phone_number"],
            password=validated_data["password"],
            is_active=False,
        )

        return user_object


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "mobile",
            "first_name",
            "last_name",
        ]


class UpdateUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(mobile=data["phone_number"]).exists():
            raise serializers.ValidationError(
                "User with this mobile number  already exists"
            )

        return data


class   LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            # Retrieve the user object based on the provided email
            user = User.objects.get(email=data["email"].lower())
        except:
            raise serializers.ValidationError(
                "User with this email {} not exists".format(data["email"])
            )
        
        # Check if the provided password matches the user's password
        if user.check_password(data["password"]):
            return data
        
        else:
            raise serializers.ValidationError("invalid password ")


class LoginResponseSerializer(serializers.Serializer):
    user_profile = serializers.SerializerMethodField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def get_user_profile(self, profile):
        # Check the user_type field of the user_profile object
        if profile["user_profile"]:
            # If user_type is 10 (organization), serialize using OrganizationProfileSerializer
            return UserProfileSerializer(profile["user_profile"]).data
        
        else:
            return None


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password do not match."
            )

        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, data):
        try:
            # Retrieve the user object based on the provided email
            user = User.objects.get(email=data["email"].lower())
            # Generate the subject and message for the password reset email
            subject_message_obj = get_set_password_subject_message(
                id=string_encrypt(str(user.uuid)),
                frontend_redirect_url=settings.EMAIL_URL,
            )
            # Send the password reset email using SendInBlueEmail class

        except:
            raise serializers.ValidationError(
                "User with this email {} not exists".format(data["email"])
            )

        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if needed
        # token['claim'] = value

        return token


class ForgotPasswordResetSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        try:
            # Check if a user with the provided UUID exists
            User.objects.get(uuid=decrypt_string(data["uuid"]))
        except:
            raise serializers.ValidationError("Invalid uuid")
        # Check if the new password and confirm password match
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "password and confirm password are not same"
            )
        return data

    def create(self, validated_data):
        # Retrieve the user object based on the decrypted UUID
        user = User.objects.get(uuid=decrypt_string(validated_data["uuid"]))
        # Set the new password for the user and save the changes
        user.set_password(validated_data["new_password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
