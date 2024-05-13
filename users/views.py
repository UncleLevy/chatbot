from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, AuthUserSerializer, ChatSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from chat.models import Chat

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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(username__iexact = request.user)
        return Response({"data": {"balance": user.token }, "message": "Balance retrieved successfully"}, status=200)


class Messages(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        messages = Chat.objects.filter(user=user)
        return Response({"messages": messages}, status=200)
    
    def post(self, request):
        message = request.data.get("message")  
        user = User.objects.get(username=request.user.username)
        if user.token > 0:
            raw_message = Chat.objects.create(user=user, message=message, response="AI dummy Response!")
            raw_message.save()
            serializedMessage = ChatSerializer(raw_message)
            user.token -= 100
            user.save()
            return Response({"message": serializedMessage.data}, status=200)
        else:
            return Response({"message": "You have depleted your tokens"}, status=400)