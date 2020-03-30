
from django.urls import path, include
from rest_framework import routers
from rest_framework.urls import url
from .api import MessageViewSet, SentMessageListView, ReceivedMessageListView, BlockUserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'api/message', MessageViewSet)
router.register(r'api/block', BlockUserViewSet)

urlpatterns = [
    url(r'api/message/sent', SentMessageListView.as_view()),
    url(r'api/message/received', ReceivedMessageListView.as_view()),
]

urlpatterns += router.urls