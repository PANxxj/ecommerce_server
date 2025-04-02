# views.py
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apps.helper import functions,status_code
from .serializers import RegisterUserSerializer,CreateUserSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            errors = functions.error_message_function(errors)
            return Response(functions.ResponseHandling.failure_response_message('error',errors),status=status_code.status400)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        context = {
            "access_token":access_token,
            "refresh_token":refresh_token,
            'user_type':user.user_type,
            "user_id":user.id,
            'user':serializer.data
            # "user_data" : user_data.data                 
        }
        
        return Response(functions.ResponseHandling.success_response_message('Accepted',context),status=status_code.status202)
    
 
 
class UserLogin(APIView):
    def post(self,request):
        print('data',request.data)
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(request,email=email,password=password)
            if user:
                login(request,user)
                refresh = RefreshToken.for_user(user)
                ser = CreateUserSerializer(user).data
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                context = {
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    'user_type':user.user_type,
                    "user_id":user.id,
                    "user":ser
                    # "user_data" : user_data.data                 
                }
              
                return Response(functions.ResponseHandling.success_response_message('Accepted',context),status=status_code.status202)
            else:
                message = {"message":"Invalid Credential"}
                return Response(message,status=status_code.status400)
        except Exception as e:
            print('error',e)
            message = {"message":"Invalid Credential"}
            return Response(message,status=status_code.status400)