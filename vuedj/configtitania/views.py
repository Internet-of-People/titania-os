from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import list_route

from .models import Config
from .serializers import ConfigSerializer

def index(request):
    return render(request, 'index.html')

class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer

    @list_route(methods=['delete'])
    def clear_todos(self, request):
        configinfo = Config.objects.all()
        configinfo.delete()
        return HttpResponse(status=200)
        # It may be a good idea here to return [].  Not sure.
