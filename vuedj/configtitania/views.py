from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import list_route

from .models import User, Schema
from .serializers import UserSerializer, SchemaSerializer

import common

@csrf_exempt
def handle_config(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        action = request.POST.get("_action")
        if action == 'getSchema':
            print(action)
            queryset = Schema.objects.all()
            schemaSet = len(queryset)
            if schemaSet == 0:
                setSchema = Schema(version=common.VERSION, major_version=common.MAJOR_VERSION, minor_version=common.MINOR_VERSION)
                setSchema.save()
                print('saved schema')
            serializer = SchemaSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif action == 'getUserDetails':
            print(action)
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif action == 'saveUserDetails':
            print(action)
            boxname = request.POST.get("boxname")
            username = request.POST.get("username")
            password = request.POST.get("password")
            setUser = User(boxname=boxname, username=username, password=password)
            setUser.save()
            return JsonResponse([{"STATUS":"SUCCESS"},{"RESPONSE":"Config saved successfully"}], safe=False)
        elif action == 'login':
            print(action)
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username+' '+password)
            queryset = User.objects.all().first()
            if username == queryset.username and password == queryset.password:
                return JsonResponse({"STATUS":"SUCCESS", "username":queryset.username}, safe=False)
            else:
                return JsonResponse({"STATUS":"FAILURE"}, safe=False)
        elif action == 'logout':
            print(action)
            username = request.POST.get("username")
            print(username+' ')
            queryset = User.objects.all().first()
            if username == queryset.username:
                return JsonResponse({"STATUS":"SUCCESS", "username":queryset.username}, safe=False)
        return JsonResponse(serializer.errors, status=400)

def index(request):
    return render(request, 'index.html')

#not being used
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#not being used
class SchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    """Setting Schema"""
    setSchema = Schema(version=common.VERSION, major_version=common.MAJOR_VERSION, minor_version=common.MINOR_VERSION)
    setSchema.save()

    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
