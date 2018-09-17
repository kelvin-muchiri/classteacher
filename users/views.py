from rest_framework.status import(
     HTTP_200_OK,
     HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,

)

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from users.serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserSerializer,
    MeSerializer
)

from users.models import User

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = MeSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_200_OK)

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

class UserLoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer= UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)