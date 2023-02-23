from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile
from .helpers import *

class LoginView(APIView):
    
    def post(self, request):
        response={}
        response['status']=500
        response['message']='Something Went wrong'
        
        try:
            data=request.data
            
            if data.get('username') is None:
                response['message']='key username not found'
                raise Exception("key username not found")
                
            if data.get('password') is None:
                response['message']='key password not found'
                raise Exception("key password not found")
            
            
            #Check Username
            
            check_user = User.objects.filter (username= data.get('username')).first()
            
            if check_user is None:
                response['message']='invalid Username' 
                raise Exception('invalid username')
            
            if not Profile.objects.filter(user= check_user).first().is_verified:
                response['message']='User not verified' 
                raise Exception('User not verified')
                
            #Check Password
            
            user_obj=authenticate(username=data.get('username'), password=data.get('password'))
            
            if user_obj:
                login(request, user_obj)
                response['status']=200
                response['message']='Password Accepted'
            else:
                response['message']='invalid Password' 
                raise Exception('invalid Password')
            
        
        except Exception as e:
            print(e)
            
        return Response(response)
       
       
LoginView = LoginView.as_view()     
        

class RegisterView(APIView):
    
    def post(self, request):
        response={}
        response['status']=500
        response['message']='Something Went wrong'
        
        try:
            data=request.data
            
            if data.get('username') is None:
                response['message']='key username not found'
                raise Exception("key username not found")
                
            if data.get('password') is None:
                response['message']='key password not found'
                raise Exception("key password not found")
            
            
            #Create Username
            
            check_user = User.objects.filter (username= data.get('username')).first()
            
            if check_user:
                response['message']='Username already taken' 
                raise Exception('Username already taken')
            
            user_obj= User.objects.create(email=data.get('username'), username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            
            token= gen_random_string(20)
            
            Profile.objects.create(user= user_obj, token= token, is_verified=True)
            # send_mail_to_user(token, data.get('username'))
            response['message']='User Created'
            response['status']=200
            
            
        
        except Exception as e:
            print(e)
            
        return Response(response)
    
RegisterView = RegisterView.as_view()