from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Campsite, Reservation, UserMessage
from .forms import ReservationForm, MessageForm
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
    
    if request.method == 'POST' and form.is_valid():
        user_message = form.cleaned_data.get('message')
        user_message_instance = UserMessage.objects.create(message=user_message)
        
        # 在这里实现聊天机器人的交互，并存储回应
        # ...
        
        user_message_instance.response = '您好，功能即将上线，敬请期待。'
        user_message_instance.save()
    
    return render(request, 'chat_channel/chatbot.html', {'form': form})