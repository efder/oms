from django.db import models

class Message(models.Model):
    # User who sent the message
    sender = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, related_name='sender_user', null=True
    )
    # User who received the message
    receiver = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, related_name='receiver_user', null=True
    )
    # Date when the message sent
    date = models.DateTimeField(
        auto_now_add=True
    )
    # Content of the message
    content = models.TextField()


class Block(models.Model):
    # User who blocks the other user
    blocking_user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='blocking_user', null=False
    )
    # User who is blocked
    blocked_user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='blocked_user', null=False
    )
