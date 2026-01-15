from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    #Registration of a new user
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CurrentUserAPIView(APIView):
    #Get current authenticated user details
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LogoutAPIView(APIView):
    #Logout the current user
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"message": "Déconnexion réussie"}, 
            status=status.HTTP_200_OK
        )