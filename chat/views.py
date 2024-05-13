from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.throttling import AnonRateThrottle
from.models import Chat
from users.models import User
from.serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated

class Messages(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(username__iexact = request.user)
        messages = Chat.objects.filter(user = user)
        return Response({"data": {"messages": messages }, "message": "Message Successfully retrived"}, status=200)
    
    def post(self, request):
        message = request.POST.get("message")
        user = User.objects.get(username__iexact = request.user)
        if user.token > 0 :
            raw_message = Chat.objects.create(user=user,message=message, response="AI dummy Response!" )
            raw_message.save()
            serializedMessage = ChatSerializer(raw_message)
            user.token -= 100
            user.save()
            print("This this is post")
            return Response({"data": {"message":  serializedMessage.data }, "message": "Balance retrieved successfully"}, status=200)
    
        else:
            return Response({"data": { }, "message": "YOu have depleted your tokens"}, status=400)
    
