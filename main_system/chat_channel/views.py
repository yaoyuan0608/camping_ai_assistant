from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Campsite, Reservation, UserMessage
from .forms import ReservationForm, MessageForm
from django.http import JsonResponse
import subprocess
import json
from django.views.decorators.csrf import csrf_exempt
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from .response import CampingChatbot
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

import time
from typing import List, Tuple
from langchain import OpenAI
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .response import CampingChatbot

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAPI_KEY")
persist_directory = 'chat_channel/static/db'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)
vectorstore = vectordb
chat = CampingChatbot(vectorstore)


def home(request):
    return render(request, "chat_channel/camping_home.html")

def homepage(request):
    return render(request, "chat_channel/homepage.html")

def chatbot(req):
    return HttpResponse('<h1>欢迎进入露营</h1>')


@login_required
def reservation_view(request):
    # redirect to other page if user is logged in
    # if request.method == 'POST':
    #     form = ReservationForm(request.POST)
    #     # if form.is_valid():
    #     # form.save()
    # else:
    form = ReservationForm()
    context = {'form': form}
    return render(request, 'chat_channel/reservation.html', context)

@login_required
def chatbot(request):
    form = MessageForm(request.POST or None)
    response_message = ''

    if request.method == 'POST' and form.is_valid():
        form_data = request.POST.dict()
        user_message = form_data.get('message')

        if user_message:
            response_message = chat.receive_message(user_message)
            print(response_message)
        else:
            response_message = 'Hi, how can I help you?'

        return JsonResponse({'message': response_message}, safe=False)
    else:
        return render(request, 'chat_channel/chatbot.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            # Change 'home' to the name of the view you want to redirect the user to after signup
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat_channel/signup.html', {'form': form})
