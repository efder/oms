from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
import logging

logger = logging.getLogger('django')

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Get the username from the request data
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        serializer = self.get_serializer(data=request.data)
        
        # The user exists and entered wrong password, then log it
        if User.objects.filter(username=username).exists() \
            and password is not None \
            and not serializer.is_valid(): 
            logger.warning('Invalid Login: %s tried to enter with wrong credentials' % username)
            raise ValidationError(detail=serializer.errors, code=400)
        
        # User succesfully logs in
        serializer.is_valid(raise_exception=True)
        logger.info('Successful Login: %s logged in succesfully' % username)

        
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })