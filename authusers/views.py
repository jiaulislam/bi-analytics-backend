from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from core.helper import EmptySerializer, enveloper
from core.metadata.openapi import OpenApiTags
from core.renderer import CustomRenderer

from .filter import UserFilter
from .models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer]
    filter_backends = [filters.DjangoFilterBackend]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.all().order_by("-created_at")

    @extend_schema(
        responses=enveloper(UserSerializer, many=True), tags=[OpenApiTags.Users]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses=enveloper(UserSerializer, many=False), tags=[OpenApiTags.Users]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses={204: enveloper(EmptySerializer, many=False)},
        tags=[OpenApiTags.Users],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    renderer_classes = (CustomRenderer,)

    @extend_schema(
        tags=[OpenApiTags.Token],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            current_user = User.objects.get(username=request.data.get("username"))
            user = UserSerializer(instance=current_user)
            payload = user.data
            payload["designation"] = current_user.profile.designation
            payload["access_token"] = serializer.validated_data.get("access")
            payload["refresh_token"] = serializer.validated_data.get("refresh")
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e
        except User.DoesNotExist:
            raise

        return Response(payload, status=status.HTTP_200_OK)
