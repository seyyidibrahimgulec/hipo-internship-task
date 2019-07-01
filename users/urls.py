from django.urls import path
from users.views import UserRegistrationView, UserAuthenticationView, MyProfileDetailView, ChangePasswordView

urlpatterns = [
    path('api/profiles/create/', UserRegistrationView.as_view(), name='create-user'),
    path('api/profiles/authenticate/', UserAuthenticationView.as_view(), name='authenticate-user'),
    path('api/profiles/me/', MyProfileDetailView.as_view(), name='my-profile-detail'),
    path('api/profiles/me/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
