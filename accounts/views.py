from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# from accounts.models import User 
from .serializer import RegisterSerializer, UserSerializer,LoginSerializer
from rest_framework_simplejwt.views import TokenRefreshView

# ✅ Dynamically get the user model
User = get_user_model()

# Register API
class RegisterApi(generics.CreateAPIView):
     # serializer_class is a attribute to access get_serializer
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                 return Response({
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                     "message": "User created successfully. Now perform login to get your token.",
            }, status=status.HTTP_201_CREATED)
            else:
               return Response({
                "message":"Data is Invalid"
             },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message":"user already exists"
            },status=status.HTTP_406_NOT_ACCEPTABLE)

# login and give access and refresh token
class LoginApi(generics.GenericAPIView):
    # serializer_class is a attribute to access get_serializer
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
        # serializer returns 'access' and 'refresh' tokens
          tokens = {
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
          }
          if tokens:
            user_data = {
               'id': serializer.validated_data['user'].id,
               'email': serializer.validated_data['user'].email,
               'username': serializer.validated_data['user'].username,
               }
            return Response({
            "message":"successully login",
            'tokens': tokens,
            'user': user_data
            }, status=status.HTTP_200_OK)
          else:
              return Response({
               "message":"Token not generated"
           }, status=status.HTTP_403_FORBIDDEN)
          # if data is invalid
        else:
            return Response({
                "message":"Credentials are invalid"
            }, status=status.HTTP_401_UNAUTHORIZED) 

# profile api -one can access who have bearer token
class ProfileApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_serializer = UserSerializer(user)
        profile_data = {
            'username': profile_serializer.data['username'],
            'first_name': profile_serializer.data['first_name'],
            'last_name': profile_serializer.data['last_name'],
            'email': profile_serializer.data['email'],
            'address': profile_serializer.data.get('address'),
            'phone': profile_serializer.data.get('phone'),
        }
        return Response({
            "profile": profile_data,
            "message": "Your profile fetched successfully"
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  # partial update
        if serializer.is_valid():
            serializer.save()
            return Response({
                "profile": serializer.data,
                "message": "Profile updated successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenRefreshView(TokenRefreshView):
#     permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception:
            return Response({
                "message": "Refresh token is invalid or expired"
            }, status=status.HTTP_401_UNAUTHORIZED)    