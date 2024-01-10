from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer
from services.user_db import get_or_create_token


class LoginView(ObtainAuthToken):
    """
    View for user login.
    - Extends ObtainAuthToken for token-based authentication.
    - Returns token and username on successful login.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.validated_data['user']
            get_or_create_token(user)
            return Response({'token': user.auth_token.key, 'username': user.username})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    """
    View for user registration.
    - Allows any user to sign up.
    - Returns user details on successful registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    View for user logout.
    - Requires token authentication.
    - Deletes user's authentication token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'detail': 'Successfully logged out.'})
