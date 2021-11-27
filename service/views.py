from service.models import *
from service.serializers import *

import datetime
import io
import json

from urllib.request import Request

from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Count
from django.contrib.auth import authenticate, logout
from django.utils.crypto import get_random_string

from rest_framework.parsers import JSONParser
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter





def index(request):
    return render(request, 'service/index.html', context={
        # 'error': True,
        # 'statusCode': 500,
        # 'message': 'test message'
    })

def generate_card_number():
    number = get_random_string(length=6, allowed_chars='1234567890')
    if Client.objects.filter(card_number=number).count() >0:
        generate_card_number()
    else:
        return number

class RegisterClientView(generics.CreateAPIView):
    serializer_class = RegisterClientSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = {}
        serializer = RegisterClientSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            card_number = generate_card_number()
            serializer.save(card_number=card_number)

            data["response"] = "Successfully added"
            data['client'] = serializer.data
            data['client']['card_number'] = card_number

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny] #isauth

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [AllowAny] #isauth
    queryset = Client.objects.all()

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny] #isauth

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]  # isauth

class InstructorListCreateView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny] #isauth

class InstructorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny] #isauth

class LoginAuthTokenView(APIView):
    permission_classes = []

    def post(self, request):
        data = {}

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            data['response'] = 'Successfully authenticated.'
            data['pk'] = user.pk
            data['username'] = user.username
            data['token'] = token.key
            resp = Response(data, status=status.HTTP_200_OK)
            resp.set_cookie('token', token.key, httponly=True)
            return resp
        else:
            data['response'] = 'Error'
            data['error_message'] = 'Invalid username or password. Try again.'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def LogoutUserView(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')

class IntervalListCreateView(generics.ListCreateAPIView):
    serializer_class = IntervalSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = Interval.objects.all()

class IntervalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IntervalSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = Interval.objects.all()



class PassTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = PassTypeSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = PassType.objects.all()

class PassTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PassTypeSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = PassType.objects.all()



class SectionTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = SectionTypeSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = SectionType.objects.all()

class SectionTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectionTypeSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = SectionType.objects.all()



class PassListCreateView(generics.ListCreateAPIView):
    serializer_class = PassSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = Pass.objects.all()

class PassDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PassSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = Pass.objects.all()



class SectionListCreateView(generics.ListCreateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = Section.objects.all()

class SectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]  # isauth
    queryset = Section.objects.all()

