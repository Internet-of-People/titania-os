from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import list_route

from .models import User, Schema
from .serializers import UserSerializer, SchemaSerializer

import common

def index(request):
    return render(request, 'index.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    """Setting Schema"""
    setSchema = Schema(version=common.VERSION, major_version=common.MAJOR_VERSION, minor_version=common.MINOR_VERSION)
    setSchema.save()

    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
