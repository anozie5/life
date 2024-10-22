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
        validated_data.pop('is_active', None)
        validated_data.pop('is_staff', None)

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

        # refresh = RefreshToken.for_user(user)
        # return {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token)
        # }

        
#serializer for user login
class LogInSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)

    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('User with this email does not exist.')

            if not user.check_password(password):
                raise serializers.ValidationError('Incorrect password.')

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Both email and password are required.')

        return attrs




    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     token['email'] = user.email
    #     return token

    # class Meta:
    #     model = User
    #     fields = ['email', 'password']


#serializer for user token
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['tokens']