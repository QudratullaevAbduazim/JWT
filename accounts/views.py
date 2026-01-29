from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import ChangePasswordSerializer, SignUpSerializer, ProfileUpdateSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from .utility import check_email
import random
from .models import VerifyCode
# Create your views here.

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    queryset = User
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = {
            'status': status.HTTP_201_CREATED,
            'username': serializer.data['username'],
            'message': 'Akkount yaratildi'
        }
        return Response(data=data)

        
class LoginView(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user is None:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'Bizda bunaqa user mavjud emas'})
        user = user.check_password(password)
        if not user:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'PArolingiz xato'})
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, 'message': 'Bizda bunaqa user mavjud emas'})
        
        refresh = RefreshToken.for_user(user)
        
        data = {
            'status': status.HTTP_200_OK,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Siz tizimga kirdingiz'
        }
        
        return Response(data=data)
        
        
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        refresh = self.request.data.get('refresh_token')
        refresh = RefreshToken(refresh)
        refresh.blacklist()
        data = {
            'success': True,
            'message': 'Siz tizimdan chiqdingiz'
        }
        return Response(data)
        


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        
        data = {
            'status': status.HTTP_200_OK,
            'username': user.username,
            'first_name': user.first_name
        }
        return Response(data)
    
    
class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            
            data = {
                'status': status.HTTP_200_OK,
                'username': user.username,
                'first_name': user.first_name,
                'message': 'Malumotlar yangilandi'
            }
            return Response(data)
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'ERROR'
        }
        return Response(data)
    
    
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user = self.request.user
        old_password = serializer.validated_data.get('old_password')
        if not user.check_password(old_password):
            raise ValidationError({"success": False, 'message': 'Eski parol xato'})
        
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Parol muvaffaqiyatli yangilandi'
        }
        return Response(data)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        email = self.request.data.get('email')
        email = check_email(email)
        if email:
            user = User.objects.filter(email=email).first()
            if user is None:
                raise ValidationError('Bu email bizda mavjud emas')

            code = random.randint(1000, 9999)

            VerifyCode.objects.create(
                user = user,
                code = code
            )
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Kodinggiz yuborildi'
            }

        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Xatolik'
        }
        return Response(data)


class ResetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError('Xatolik')

        user = request.user
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')


        if not user.check_password(old_password):
            raise ValidationError({
                'success': False,
                'message': 'Eski parol xato'
            })
        user.set_password(new_password)
        user.save()

        return Response({
            'success': True,
            'message': 'Parol muvaffaqiyatli yangilandi',
        })





            
                
                
        
    
