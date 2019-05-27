import requests
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Joke
from core.serializers import JokeSerializer, SighupUserSerializer


class GenerateJokeView(APIView):

    @swagger_auto_schema(
        responses={201: openapi.Response(
            description='Joke generated successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'text': openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=['text']
            )
        )})
    def post(self, request, *args, **kwargs):
        response = requests.get(settings.API_JOKES_GENERATOR)
        return Response({'text': response.json()}, status=status.HTTP_201_CREATED)


class JokeView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = JokeSerializer

    def get_queryset(self):
        return self.request.user.jokes.all()


class JokeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JokeSerializer
    http_method_names = ['options', 'get', 'put', 'delete']

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.request.user.jokes.all()
        else:
            return Joke.objects.none()

    def perform_destroy(self, instance):
        self.request.user.jokes.remove(instance)


class SighupView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SighupUserSerializer
