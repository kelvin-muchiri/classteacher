"""
User Serializers
"""
from django.db import transaction
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users import models

from common.utilities import validate_phone_number

class MeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        phone_number = attrs.get('phone_number', False)
        email = attrs.get('email', False)

        if not (phone_number or email):
            raise serializers.ValidationError(
                'A phone number or email is required'
            )

        return attrs

    class Meta:
        model = models.User
        fields = (
            'id',
            'first_name',
            'last_name',
            'other_names',
            'full_name',
            'phone_number',
            'email',
            'gender',
            'date_of_birth',
            'date_joined',
            'last_login',
            'token',
        )

        read_only_fields = (
            'token',
            'last_login',
            'date_joined',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'first_name',
            'last_name',
            'other_names',
            'full_name',
            'username',
        )


class UserInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'full_name',
            'username',
            'gender',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True,
        error_messages={
            'blank': 'This field is required'
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=255,
        error_messages={
            'blank': 'This field is required',
            'min_length': 'Password is too short',
            'max_length': 'Password is too long'
        }
    )

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get('password', None)
        confirm_password = value

        if password != confirm_password:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        return value

    def validate_email(self, value):
        if value and models.User.objects.filter(
                email=value, is_deleted=False).exists():
            raise serializers.ValidationError(
                'A user with that email already exists'
            )

        return value

    def validate_phone_number(self, value):
        if value:
            validate_phone_number(value)

        if value and models.User.objects.filter(
                phone_number=value, is_deleted=False).exists():
            raise serializers.ValidationError(
                'A user with that phone number already exists'
            )

        return value

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', False)
        email = attrs.get('email', False)

        if not (phone_number or email):
            raise serializers.ValidationError(
                'A phone number or email is required to register'
            )

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user_model_fields = [f.name for f in models.User._meta.get_fields()]
        valid_user_data = {
            key: validated_data[key]
            for key in user_model_fields
            if key in validated_data.keys()
        }
        user = models.User.objects.create_user(**valid_user_data)

        return user

    class Meta:
        model = models.User
        fields = (
            'id',
            'first_name',
            'last_name',
            'other_names',
            'username',
            'email',
            'password',
            'confirm_password',
            'phone_number',
            'gender',
            'date_of_birth',
            'token',
        )

        extra_kwargs = {
            'first_name': {
                'error_messages': {
                    'blank': 'This field is required'
                }
            },
            'phone_number': {
                'validators': [UniqueValidator(
                    queryset=models.User.objects.all(),
                    message='A user with this phone number already exists'
                )]
            },
            'email': {
                'validators': [UniqueValidator(
                    queryset=models.User.objects.all(),
                    message='A user with this email already exists'
                )]
            },
            'username': {
                'validators': [UniqueValidator(
                    queryset=models.User.objects.all(),
                    message='A user with this username already exists'
                )],
                'error_messages': {
                    'blank': 'This field is required'
                }
            }
        }


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'blank': 'This field is required'
        }
    )
    details = MeSerializer(read_only=True)

    def validate_email(self, value):
        if 'email' in self.get_initial() and not value:
            raise serializers.ValidationError(
                'This field is required '
            )

        return value

    def validate_phone_number(self, value):
        if 'phone_number' in self.get_initial() and not value:
            raise serializers.ValidationError(
                'This field is required '
            )

        return value

    def validate(self, attrs):
        email = attrs.get('email', None)
        phone_number = attrs.get('phone_number', None)
        password = attrs.get('password', None)

        if not (email or phone_number):
            raise serializers.ValidationError(
                'An email or phone number is required to log in.'
            )
        if email:
            user = authenticate(username=email, password=password)
        elif phone_number:
            user = authenticate(username=phone_number, password=password)
        else:
            raise serializers.ValidationError(
                'How the hell did we get here'
            )

        if user is None:
            raise serializers.ValidationError(
                'Incorrect credentials'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
            'details': user
        }

    class Meta:
        model = models.User
        fields = (
            'phone_number',
            'email',
            'password',
            'token',
            'details',
        )