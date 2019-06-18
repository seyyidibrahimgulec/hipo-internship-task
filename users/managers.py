from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        user = self.model(email=email, username=username, is_superuser=False, is_staff=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.model(email=email, username=username, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save(using=self._db)
        return user
