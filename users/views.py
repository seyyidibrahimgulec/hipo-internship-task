# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
from rest_framework import viewsets, generics
from .models import UserProfile
from .serializers import UserSerializer, CreateUserSerializer, CustomAuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated, IsOwnerOrIsAdmin)


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

# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'


class MyProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    # def get(self, request, *args, **kwargs):
    #     user = self.request.user
    #     return Response({
    #         'username': user.username,
    #         'email': user.email,
    #     })

