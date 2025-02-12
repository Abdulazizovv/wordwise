from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'botuser', BotUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]