from .serializers import *
from .models import *
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView 

# Create your views here.
#sign up view
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate incoming data
        user = serializer.save()  # Call create method in the serializer

        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),  # Return refresh token
            'access': str(refresh.access_token),  # Return access token
            'user': serializer.data  # Include user data in the response
        }, status=status.HTTP_201_CREATED)

#login view
class LoginView(TokenObtainPairView):
    serializer_class = LogInSerializer

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the user object from the validated data
        user = serializer.validated_data['user']
        
        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)
        
        user_data = {
            'username': user.username,
            'email': user.email,
        }

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data  # Return serialized user data instead of the object itself
        }, status= status.HTTP_200_OK)




#token view
class TokenView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        user_token = Token.objects.get(pk=pk)
        token = UserTokenSerializer(user_token, many=False)
        return Response(token.data,  status = status.HTTP_200_OK)

    def put(self, request, pk):
        user_token = Token.objects.get(pk=pk)
        token = UserTokenSerializer(request.data, instance=user_token)
        if token.is_valid():
            token.save()
            return Response('Token updated',  status = status.HTTP_200_OK)
        return Response(token.errors, status = status.HTTP_400_BAD_REQUEST)
