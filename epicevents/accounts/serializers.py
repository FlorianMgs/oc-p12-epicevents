from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Client


User = get_user_model()


class UserSignupSerializer(ModelSerializer):

    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'tokens'
        ]

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError('User already exists')
        return value

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise ValidationError('Password is empty')

    def get_tokens(self, user: User) -> dict:
        tokens = RefreshToken.for_user(user)
        data = {
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
        ]


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'date_created',
            'date_updated',
            'sales_contact'
        ]

