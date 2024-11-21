from django.shortcuts import redirect, render

from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import render,  redirect
from django.http import HttpResponse, JsonResponse  
from .models import *

import random
# Create your views here.

class UserView(viewsets.ModelViewSet):
    queryset =  User.objects.all()
    serializer_class = UserSerializer

from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:  # Ensure passwords match
            user = User.objects.create_user(
                username=username,
                first_name=fname,
                last_name=lname,
                email=email,
            )
            user.set_password(pass1)  # Hash password before saving
            user.save()
            messages.success(request, 'Your account was successfully created')
            return redirect('/signin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('/signup')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        print(f"Username: {username}, Password: {pass1}")  # Debug
        user = authenticate(username=username, password=pass1)

        if user is not None:
            print("User authenticated")
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('quizapp:home')
        else:
            print("Authentication failed")
            messages.error(request, 'Bad credentials')
            return redirect('/signin')
    return render(request, 'signin.html')
 
def search(request):
    query = request.GET.get('search')
    results = []
    if query:
        results = User.objects.filter(Q(username__icontains = query) | Q(fname__icontains = query) | Q(lname__icontains = query))
        messages.success(request, 'search was successful')
        return render(request, 'home.html',{'results':results,'query':query,'messages':messages})
    else:
        messages.error(request, 'Enter a search item')
    

def home(request):
    context = {'catgories': Types.objects.all()}
    
    if request.GET.get('gfg'):
        return redirect(f"/quiz/?gfg={request.GET.get('gfg')}")
    
    return render(request, 'home.html', context)

def quiz(request):
    context = {'gfg': request.GET.get('gfg')}
    return render(request, 'quiz.html', context)



def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        
        if request.GET.get('gfg'):
            question_objs = question_objs.filter(gfg__gfg_name__icontains = request.GET.get('gfg'))
            
        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)
        
        
        for question_obj in question_objs:
            
            data.append({
                "uid" : question_obj.uid,
                "gfg": question_obj.gfg.gfg_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answer" : question_obj.get_answers(),
            })

        payload = {'status': True, 'data': data}
        
        return JsonResponse(payload)  # Return JsonResponse
        
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")
    

def logout(request):
    
    return render(request, 'logout.html')