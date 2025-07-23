from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Videojuego
from .serializers import VideojuegoSerializer
from django.shortcuts import get_object_or_404

class VideojuegoListCreateAPIView(APIView):
 
    def get(self, request):
        videojuegos = Videojuego.objects.all()
        serializer = VideojuegoSerializer(videojuegos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = VideojuegoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideojuegoDetailAPIView(APIView):
    def get(self, request, pk):
        videojuego = get_object_or_404(Videojuego, pk=pk)
        serializer = VideojuegoSerializer(videojuego)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        videojuego = get_object_or_404(Videojuego, pk=pk)
        serializer = VideojuegoSerializer(videojuego, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        videojuego = get_object_or_404(Videojuego, pk=pk)
        videojuego.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)