from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.models import Joke


class JokeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Joke
        fields = ['id', 'text']
        extra_kwargs = {
            'text': {'max_length': 10000},
        }

    def create(self, validated_data):
        user = self.context.get('request').user
        joke_instance, created = Joke.objects.get_or_create(text=validated_data.get('text'))
        user.jokes.add(joke_instance)
        return joke_instance

    def update(self, instance, validated_data):
        if instance.users.count() == 1:
            return super().update(instance, validated_data)
        else:
            user = self.context.get('request').user
            instance.users.remove(user)
            return self.create(validated_data)


class SighupUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password')
        )
        Token.objects.create(user=user)
        return user
