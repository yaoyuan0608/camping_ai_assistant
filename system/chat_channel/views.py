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

# Create your views here.
import time
# Create your views here.
# os.environ['OPENAI_API_KEY'] =
# loader = TextLoader("./chat_channel/static/data/camp_knowledge.txt")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(
#     chunk_size=1000, separator="\n", chunk_overlap=0)
# documents = text_splitter.split_documents(documents)
os.environ['OPENAI_API_KEY'] = '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'
persist_directory = 'chat_channel/static/db'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)
vectorstore = vectordb  # 使用前面的方法创建一个Chroma对象
chat = CampingChatbot(vectorstore)


def home(request):
    return render(request, "chat_channel/camping_home.html")


def homepage(request):
    return render(request, "chat_channel/homepage.html")


def chatbot(req):
    return HttpResponse('<h1>欢迎进入露营</h1>')


@login_required
def reservation_view(request):
    # if request.method == 'POST':
    #     form = ReservationForm(request.POST)
    #     # if form.is_valid():
    #     # form.save()
    #     # 这里可以添加预定成功后的操作，例如重定向到其他页面
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
