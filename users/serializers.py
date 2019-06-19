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

    def validate_password(self, password):
        validators.validate_password(password=password, user=UserProfile)
        return password

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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    def validate_new_password(self, new_password):
        validators.validate_password(new_password)
        return new_password

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            msg = ugettext_lazy('Wrong password')
            raise serializers.ValidationError(msg, code='authorization')
        return old_password