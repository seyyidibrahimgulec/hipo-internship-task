# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
from rest_framework import generics, status
from .serializers import UserSerializer, CreateUserSerializer, CustomAuthTokenSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.models import UserProfile
from django.core.mail import send_mail
from HipoProject.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_from = EMAIL_HOST_USER
        send_mail(subject='Test', message='Test message', from_email=email_from,
                  recipient_list=['seyyidibrahimgulec@gmail.com', ], fail_silently=False,
                  html_message=render_to_string(template_name='email.html'))
        return super(UserRegistrationView, self).post(request=request)


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


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = UserProfile
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("new_password"))
        user.auth_token.delete()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
