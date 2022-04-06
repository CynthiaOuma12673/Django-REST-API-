from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.

from rest_framework import viewsets

from .serializers import HeroSerializer
from .models import Hero


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer
    permission_classes = (IsAdminOrReadOnly,)

    
    def post(self, request, format=None):
        serializers = HeroSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class HeroViewSetAlias(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    def get_hero(self, pk):
        try:
            return HeroViewSet.objects.get(pk=pk)
        except HeroViewSet.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        hero = self.get_hero(pk)
        serializers = HeroSerializer(hero)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        hero = self.get_hero(pk)
        serializers = HeroSerializer(hero, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        hero = self.get_hero(pk)
        hero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
def home(request):
    return render(request, 'index.html')
