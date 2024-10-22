from .models import *
from rest_framework import serializers
# from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#serializer for user creation
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','age','email','password','is_active','is_staff']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True}
        }

        def create(self, validated_data):
            user = super().create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            # return user

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return {'refresh': str(refresh), 'access': token}

        
#serializer for user login
class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        return token

    class Meta:
        model = User
        fields = ['email', 'password']

# class LogInSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email','password']
    
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['email'] = user.email
#         return token


#serializer for user token
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['tokens']