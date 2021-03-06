from service.models import *
from service.serializers import *
from service.permission import *

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
from django.utils.decorators import method_decorator

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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



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

    @swagger_auto_schema(operation_id="lalala")
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

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id="xdddddd"
))
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsReceptionistUser, IsAdministratorUser, IsInstructorUser] #isauth



class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [AllowAny] #isauth
    queryset = Client.objects.all()

    @swagger_auto_schema(operation_id="1234")
    def put(self, *args, **kwargs):
        return super(ClientDetailView, self).put(*args, **kwargs)


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdministratorUser] #isauth

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdministratorUser]  # isauth

class InstructorListCreateView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAdministratorUser] #isauth

class InstructorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAdministratorUser] #isauth

class LoginAuthTokenView(APIView):
    permission_classes = []

    def post(self, request):
        data = {}

        username = request.data.get('username')
        password = request.data.get('password')
        user = Instructor.objects.filter(username=username, password=password).first()
        if user is not None:
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


