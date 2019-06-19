# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
from rest_framework import generics
from .serializers import UserSerializer, CreateUserSerializer, CustomAuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class UserAuthenticationView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
        })


class MyProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


