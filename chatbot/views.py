#chatbot/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the index page!")