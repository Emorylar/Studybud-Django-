from django.shortcuts import render, redirect #after the form is submitted , the user is redirected to home page
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse   #3.  Imports module HttpResponse which will return response to the user trying to access the url
from .models import Room, Topic, Message 
from .forms import RoomForm
# Create your views here.

'''
rooms=[                                           #10.rooms is a list with dictionary as object
    {'id':1 , 'name':'Lets learn python!'},
    {'id':2 , 'name':'Design with me'},
    {'id':3 , 'name':'Front end developers'},
]'''

# FUNCTION BASED VIEW

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')

    context={'page':page}
    return render (request,'base/login_register.html', context)

def logoutUser(request):
    logout(request)      #will delete the token
    return redirect('home')

def registerPage(request):
    page='register'
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    context={'form':form}
    return render(request,'base/login_register.html',context)

def home(request):  #2. Request is that object that gets what (kind of data) the user is sending to the backend
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)         |
        Q(description__icontains=q)
         )                                    #12. query for Room. THIS is case insensitive. For case sensitive we can write contains instead of icontains 
    #now we can search by 3 different values they are topic name , name and description
    room_count=rooms.count()
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context={'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)    #7.....rendering templates

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html',context)

def userProfile(request, pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'rooms':rooms,'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='/login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)     #To store all the values into the form
        if form.is_valid():
            room=form.save(commit= False)                 #will create room instance but will not be saved to DB yet
            room.host= request.user                       #assign current user as host
            room.save()                                   #save the room to DB
            return redirect('home')
        
    context={'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)    #the form is prefilled with the room value

    if request.user!=room.host:
        return HttpResponse("You are not allowed here!!")
    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("You are not allowed here!!")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("You are not allowed here!!")
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})