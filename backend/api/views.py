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

#login view
class LoginView(TokenObtainPairView):
    serializer_class = LogInSerializer

    permission_classes = [AllowAny]



#signup view
# class SignUpView(generics.CreateAPIView):
#     # queryset = User.objects.all()
#     serializer_class = SignUpSerializer 

#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)
#         token = str(refresh.access_token)

#         return Response({'user': '{user} created', 'token': 'token created'}, status=status.HTTP_201_CREATED)

# #login view
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LogInSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']

#         # Authenticate the user
#         user = authenticate(email=email, password=password)

#         if user is not None:
#             # If authentication is successful, generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         else:
#             # If authentication fails, return an error response
#             return Response(
#                 {"detail": "Invalid credentials, please try again."}, 
#                 status=status.HTTP_401_UNAUTHORIZED
#             )



        # serializer.is_valid(raise_exception=True)

        # user = authenticate(
        #     email=serializer.validated_data['email'], 
        #     password=serializer.validated_data['password']
        # )
        
        # if user is not None:
        #     refresh = RefreshToken.for_user(user)
        #     return Response('User logged in successfully', status=status.HTTP_202_ACCEPTED)
        # else:
        #     return Response(
        #         {"detail": "Invalid credentials"}, 
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )





        # if user.is_valid():
        #     refresh = RefreshToken.for_user(user)
        #     token = str(refresh.access_token)
        #     # return Response({'user': user.data, 'token': token}, status=status.HTTP_202_ACCEPTED)
        #     return Response('{user.username} is logged in', status=status.HTTP_202_ACCEPTED)

# class LoginView(generics.GenericAPIView):
#     serializer_class = LogInSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']

#         refresh = RefreshToken.for_user(user)
#         token = str(refresh.access_token)

#         return Response({'user': serializer.data, 'token': token}, status=status.HTTP_200_OK)


# #signup view
# class SignUpView(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = SignUpSerializer


# #login view
# class LoginView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = LogInSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data)


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
