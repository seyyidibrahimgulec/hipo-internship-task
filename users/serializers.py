from rest_framework import serializers
from .models import UserProfile
from django.utils.translation import ugettext_lazy
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, data):
        validators.validate_password(password=data, user=UserProfile)
        return data

    def create(self, validated_data):
        password = validated_data['password']
        user = UserProfile(username=validated_data['username'], email=validated_data['email'])
        user.set_password(password)
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = UserProfile.objects.get(email=email)
                is_correct = user.check_password(password)
            except ObjectDoesNotExist:
                msg = ugettext_lazy('Incorrect email address')
                raise serializers.ValidationError(msg, code='authorization')

            if not is_correct:
                msg = ugettext_lazy('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ugettext_lazy('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

