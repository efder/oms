import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class MessageTestCase(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="sender_pw")
        self.receiver = User.objects.create_user(username="receiver", password="receiver_pw")
        self.client.force_authenticate(user=self.sender)
    
    def test_list_messages(self):
        response = self.client.get("/api/message")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_send_message_ok(self):
        data = {"receiver": "receiver", "content": "Test message"}
        response = self.client.post("/api/message", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_receiver_param_missing(self):
        data = {"content": "Test message"}
        response = self.client.post("/api/message", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_content_param_missing(self):
        data = {"receiver": "receiver"}
        response = self.client.post("/api/message", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_receiver_does_not_exist(self):
        data = {"receiver": "rcvr", "content": "Test message"}
        response = self.client.post("/api/message", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class SentMessageTestCase(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="sender_pw")
        self.receiver = User.objects.create_user(username="receiver", password="receiver_pw")
        self.client.force_authenticate(self.sender)

    def test_list_sent_messages(self):
        response = self.client.get("/api/message/sent")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_sent_messages_by_receiver_ok(self):
        response = self.client.get("/api/message/sent?receiver=receiver")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_sent_messages_by_not_existing_receiver(self):
        response = self.client.get("/api/message/sent?receiver=rcvr")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ReceivedMessageListTestCase(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="sender_pw")
        self.receiver = User.objects.create_user(username="receiver", password="receiver_pw")
        self.client.force_authenticate(self.receiver)

    def test_list_received_messages(self):
        response = self.client.get("/api/message/received")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_received_messages_by_sender_ok(self):
        response = self.client.get("/api/message/received?sender=sender")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_received_messages_by_not_existing_sender(self):
        response = self.client.get("/api/message/received?sender=sndr")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BlockUserTestCase(APITestCase):
    def setUp(self):
        self.blocking = User.objects.create_user(username="blocking", password="blocking_pw")
        self.blocked = User.objects.create_user(username="blocked", password="blocked_pw")
        self.client.force_authenticate(self.blocking)
    
    def test_block_user_ok(self):
        data = {"blocked": "blocked"}
        response = self.client.post("/api/block", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_block_blocked_param_missing(self):
        data = {}
        response = self.client.post("/api/block", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_block_blocked_user_not_exists(self):
        data = {"blocked": "blckd"}
        response = self.client.post("/api/block", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_block_send_message(self):
        data = {"blocked": "blocked"}
        response = self.client.post("/api/block", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {"receiver": "blocking", "content": "Test message"}
        self.client.force_authenticate(self.blocked)
        response = self.client.post("/api/message", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)