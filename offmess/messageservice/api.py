from rest_framework import viewsets, permissions, generics, mixins
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message, Block
from .serializers import MessageSerializer, BlockSerializer
from .permissions import IsSenderOrReceiver

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
        receiver = User.objects.get(username=self.request.data['receiver'])
        # Check that if the sender is the blocked by receiver
        num_results = Block.objects.get(blocking_user=receiver, blocked_user=self.request.user)
        if num_results > 0:
            print("Heyy")
            return -1
        else:
            print("OK")
            serializer.save(sender=self.request.user, receiver=receiver)

class SentMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes= [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        receiver = self.request.query_params.get('receiver', None)
        if receiver is not None:
            # TODO: make try-except
            receiver = User.objects.get(username=receiver)
            queryset = queryset.filter(Q(sender=user) & Q(receiver=receiver))
        else:
            queryset = queryset.filter(Q(sender=user))
        return queryset

class ReceivedMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        sender = self.request.query_params.get('sender', None)
        if sender is not None:
            # TODO: make try-except
            sender = User.objects.get(username=sender)
            queryset = queryset.filter(Q(sender=sender) & Q(receiver=user))
        else:
            queryset = queryset.filter(Q(receiver=user))
        return queryset 

class BlockUserViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username=self.request.user.username)
        return queryset.filter(Q(blocking_user=user))

    def perform_create(self, serializer):
        blocked_user = User.objects.get(username=self.request.data['blocked'])
        serializer.save(blocking_user=self.request.user, blocked_user=blocked_user)





