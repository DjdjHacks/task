from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
import math, random
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime, timedelta


# Create your views here.
@login_required()
def index(request):
	context={}
	context['image']=data.objects.filter(user=request.user)
	if request.method =="POST":
		image=request.FILES['image']
		from datetime import datetime, timedelta
		time_threshold = datetime.now() - timedelta(minutes=5)
		print(time_threshold)
		if image != "" and data.objects.filter(date__lt=time_threshold).exists() == False:
			d=data.objects.create(image=image)
			d.user=request.user
			d.save()
		else:
			context['status']="can not upload image upload after 5 minutes"	
		return render(request,'project/index.html',context)
	else:		
		return render(request,'project/index.html',context)




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_login(request):
    password = request.data.get("password")
    username= request.data.get("username")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        returnMessage = {'error': 'Invalid Credentials'}
        return HttpResponse(
        json.dumps(returnMessage),
        content_type = 'application/javascript; charset=utf8'
    )
    token, _ = Token.objects.get_or_create(user=user)
    returnToken = {'token':token.key}
    w,__=wallet.objects.get_or_create(user=user)
    w.save()
    return HttpResponse(
        json.dumps(returnToken),
        content_type = 'application/javascript; charset=utf8'
    )




def login_view(request):
	context={}
	if request.user.is_authenticated:
		return redirect("/index")
	if request.method=="POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request, user)
			return redirect("/index")
			context['status']="login successfully"
		else:
			context['status']="email and password is not exists" 
		return render(request,"project/login.html",context)
	else:
		return render(request,"project/login.html",context)  