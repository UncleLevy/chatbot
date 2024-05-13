from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, AuthUserSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Account successfully created.",
                "details": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = AuthUserSerializer
    permission_classes = [AllowAny]

class TokenBalanceView(APIView):
    def get(self, request):
        return Response({"data": {"balance": 0}, "message": "Balance retrieved successfully"}, status=200)