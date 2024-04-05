from rest_framework.serializers import (
    CharField,
    ListSerializer,
    ModelSerializer,
    Serializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Trader, User, UserProfile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "last_login",
        )

    def create(self, validated_data):
        user: User = super().create(validated_data)
        passwd = validated_data.get("password")
        if passwd:
            user.set_password(passwd)
            user.save()
        return user

    def to_representation(self, instance: User):
        data = super().to_representation(instance)
        data["name"] = instance.get_full_name()
        data["profile"] = ProfileSerializer(instance=instance.profile).data
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token["username"] = user.username
        token["role"] = user.role

        return token


class TraderSerializer(ModelSerializer):
    class Meta:
        model = Trader
        fields = "__all__"


class BulkUserCreateSerializer(Serializer):
    users = ListSerializer(child=CharField())
    role = CharField()
    password = CharField(required=True)
