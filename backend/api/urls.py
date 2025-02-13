from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'botuser', BotUserViewSet)
router.register(r'words', WordViewSet)
router.register(r'wordcategories', WordCategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]