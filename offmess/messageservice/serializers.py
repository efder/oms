from rest_framework import serializers
from .models import Message, Block

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'date', )
    # Serialize only the users' usernames
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'blocking_user', 'blocked_user', )
    
    # Serialize only the usernames
    blocking_user = serializers.ReadOnlyField(source='blocking_user.username')
    blocked_user = serializers.ReadOnlyField(source='blocked_user.username')