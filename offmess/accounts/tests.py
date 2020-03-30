import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_registration_ok(self):
        data = {"username": "test_user", "password": "test_pw", "email": "test@test.com"}
        response = self.client.post("/api/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_registration_same_username(self):
        data = {"username": "test_user", "password": "test_pw", "email": "test@test.com"}
        response_first = self.client.post("/api/auth/register", data)
        response_second = self.client.post("/api/auth/register", data)
        self.assertEqual(response_first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_second.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_username_missing(self):
        data = {"password": "test_pw", "email": "test@test.com"}
        response = self.client.post("/api/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_password_missing(self):
        data = {"username": "test_user", "email": "test@test.com"}
        response = self.client.post("/api/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_pw")
        data = {"username": "test_user", "password": "test_pw"}
        response = self.client.post("/api/auth/login", data)
        self.token = json.loads(str(response.content, encoding='utf-8'))['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
    
    def test_list_messages_authenticated(self):
        response = self.client.get("/api/message")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_messages_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/message")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get("/api/message")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post("/api/auth/logout", {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 
        response = self.client.get("/api/message")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)