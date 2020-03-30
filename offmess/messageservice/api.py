from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Message, Block
from .serializers import MessageSerializer, BlockSerializer
from .permissions import IsSenderOrReceiver
import logging

logger = logging.getLogger('django')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsSenderOrReceiver,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        return queryset.filter(Q(sender=user) | Q(receiver=user))
       
    def perform_create(self, serializer):
        # Check that if receiver param was sent
        receiver_param = self.request.data.get('receiver', None)
        # If it was not sent raise exception
        if receiver_param is None:
            raise ValidationError(detail={"receiver": ["This field is required."]}, code=400)
        # Check that if the user exists
        receiver = User.objects.filter(username=receiver_param).first()
        if receiver is None:
            raise ValidationError(detail={"detail": "Receiver does not exist."}, code=400)
        # Check that if the sender is the blocked by receiver
        blocked = Block.objects.filter(blocking_user=receiver, blocked_user=self.request.user).exists()
        # The sender is blocked, do not send the message
        if blocked:
            logger.info("Blocked Message: Message from %s to %s is blocked", self.request.user.username, receiver_param)
            raise PermissionDenied(detail={"detail":  "You are blocked by " + self.request.data['receiver']})
        else:
            serializer.save(sender=self.request.user, receiver=receiver)
            logger.info("Successful Message: Message from %s to %s is sent", self.request.user.username, receiver_param)

# View for listing and querying messages sent by current authenticated user
class SentMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes= [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        receiver_param = self.request.query_params.get('receiver', None)
        if receiver_param is not None:
            receiver = User.objects.filter(username=receiver_param).first()
            if receiver is not None:
                queryset = queryset.filter(Q(sender=user) & Q(receiver=receiver))
            else:
                raise ValidationError(detail={"detail": "Receiver does not exist."}, code=400)
        else:
            queryset = queryset.filter(Q(sender=user))
        return queryset
    
# View for listing and querying messages sent to current authenticated user
class ReceivedMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        sender_param = self.request.query_params.get('sender', None)
        if sender_param is not None:
            sender = User.objects.filter(username=sender_param).first()
            if sender is not None:
                queryset = queryset.filter(Q(sender=sender) & Q(receiver=user))
            else:
                raise ValidationError(detail={"detail": "Sender does not exist."}, code=400)
        else:
            queryset = queryset.filter(Q(receiver=user))
        return queryset 

# View for blocking the users and listing blocked users of current authenticated user
class BlockUserViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        return queryset.filter(Q(blocking_user=user))

    def perform_create(self, serializer):
        # Check that if the blocked parameter exists
        blocked_param = self.request.data.get('blocked', None)
        if blocked_param is None:
            raise ValidationError(detail={"blocked":["This field is required."]}, code=400)
        # Check that if the user to be blocked exists
        blocked_user = User.objects.filter(username=blocked_param).first()
        if blocked_user is None:
            raise ValidationError(detail={"detail":"User to be blocked does not exist."}, code=400)
        # Check that if the user is already blocked
        if Block.objects.filter(blocking_user=self.request.user, blocked_user=blocked_user).exists():
            raise ValidationError(detail={"detail": "User %s has already been blocked." % blocked_param } , code=400)
        serializer.save(blocking_user=self.request.user, blocked_user=blocked_user)
        logger.info("Block User: %s blocked %s", self.request.user.username, blocked_param)