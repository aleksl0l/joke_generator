from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

from core import views
from core.views import SighupView

joke_urls = [
    path('', views.JokeView.as_view(), name='jokes'),
    path('generate/', views.GenerateJokeView.as_view(), name='generate_joke'),
    path('<int:pk>/', views.JokeDetailsView.as_view(), name='detail_joke'),
]

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='user_login'),
    path('sighup/', SighupView.as_view(), name='user_sighup'),
    path('jokes/', include(joke_urls)),
]
