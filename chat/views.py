from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle
from.models import Chat
from.serializers import ChatSerializer

class ChatView(APIView):
    throttle_classes = [AnonRateThrottle]  # Apply rate limiting

    def post(self, request): 
        token = request.headers.get('Authorization')
        if token:
            token = token.split(' ')[1]
            try:
                user = Token.objects.get(key=token).user
            except Token.DoesNotExist:
                return Response({"message": "Invalid token"}, status=401)
            
            message = request.data.get('message')
            if not message:
                return Response({"message": "Message is required"}, status=400)
            
            response = "AI Response"  # AI response 
            chat = Chat(user=user, message=message, response=response)
            chat.save()
            
            # Deduct tokens from the user's balance
            user.tokens -= 100 #Remove 100 tokens form the total
            if user.tokens < 0:
                user.tokens = 0  # Prevent negative balances
            user.save()
            
            return Response({"message": "Chat saved successfully"}, status=201)
        else:
            return Response({"message": "Token is required (FROM POST)"}, status=401)
    
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if not auth_header.startswith('Bearer '):
                return Response({"message": "Invalid token format. Expected Bearer <token>"}, status=401)
            
            token = auth_header.split(' ')[1]
            try:
                user = Token.objects.get(key=token).user
            except Token.DoesNotExist:
                return Response({"message": "Invalid token (trapped on exception)"}, status=401)
            
            chats = Chat.objects.filter(user=user).order_by('-id')
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data, status=200)
        
        return Response({"message": "Token is required (FROM GET)"}, status=401)