from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Campsite, Reservation, UserMessage
from .forms import ReservationForm, MessageForm
from ./qa/chatbot import chatbot
from django.http import JsonResponse
import subprocess
import json
from django.views.decorators.csrf import csrf_exempt
import time
# Create your views here.


def user_list(request):
    return render(request, "chat_channel/base.html")


def chatbot(req):
    return HttpResponse('<h1>欢迎进入露营</h1>')


def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            # 这里可以添加预定成功后的操作，例如重定向到其他页面
    else:
        form = ReservationForm()

    context = {'form': form}
    return render(request, 'chat_channel/reservation.html', context)


def chatbot(request):
    form = MessageForm(request.POST or None)
    response_message = ''

    if request.method == 'POST' and form.is_valid():
        form_data = request.POST.dict()
        user_chatbot = chatbot()
        user_message = form_data.get('message')
        response_message = user_chatbot.get_response(user_message)
        if response_message:
            # cmd = ['python', 'path/to/chat.py', user_message]
            # response_message = subprocess.check_output(cmd, universal_newlines=True)
            print("功能即将上线")
            response_message = response_message
        else:
            print("shabi")
            response_message = '请说出您的问题'

        return JsonResponse({'message': response_message}, safe=False)
    else:
        return render(request, 'chat_channel/chatbot.html', {'form': form})
