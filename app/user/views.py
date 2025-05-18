"""
Views for the user API.

This module contains views for user management including:
- User creation
- Authentication (login/logout)
- User profile management
"""

from typing import Any
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework import serializers
import logging
import traceback
from rest_framework.exceptions import ValidationError

from coreapp.models import User
from user.serializers import UserSerializer, AuthTokenSerializer, LogOutSerializer


logger = logging.getLogger(__name__)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system.
    
    This view handles user registration with the following features:
    - Validates user input using UserSerializer
    - Throttles registration attempts to prevent abuse
    """
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle]
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Unhandled error in registration: %s", traceback.format_exc())
            return Response(
                {"error": "Server error during registration"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginView(TokenObtainPairView):
    """Handle user login and token generation.
    
    This view uses JWT for authentication and provides a token pair (access and refresh).
    """
    serializer_class = AuthTokenSerializer
    throttle_classes = [UserRateThrottle]
    

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for user login."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Get the validated user
            user = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            # Get user data using UserSerializer
            user_data = UserSerializer(user).data


            # Return tokens and user data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            })
        except serializers.ValidationError as e:
            # Check if this is an authentication error
            if isinstance(e.detail, dict):
                for field, errors in e.detail.items():
                    if isinstance(errors, list) and any(
                        error.code == 'authorization' 
                        for error in errors
                    ):
                        return Response(
                            {'detail': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
                    raise e
                
        except Exception:
            # Log unexpected server errors
            logger.error("Unhandled error in login: %s", traceback.format_exc())
            return Response(
                {"error": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class UserLogoutView(generics.GenericAPIView):
    """Handle user logout and token blacklisting.
    
    This view allows users to log out by blacklisting their refresh token.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = LogOutSerializer
    
    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for user logout."""
        try:
            # Get the user's refresh token
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'detail': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            RefreshToken(refresh_token).blacklist()
            
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.ListAPIView):
    """Handle user profile retrieval and update.
    
    This view allows authenticated users to view and update their profile information.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    
    def get_object(self):
        """Get the current user object."""
        return self.request.user
    

class UserListView(generics.ListAPIView):
    """Handle listing all users.
    
    This view allows authenticated users to view a list of all users in the system.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    
    
    def get_queryset(self):
        """Get the list of all users."""
        return self.queryset.all()
    
class UserProfileUpdateView(generics.UpdateAPIView):
    """Handle user profile update.
    
    This view allows authenticated users to update their profile information.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self):
        """Get the current user object."""
        return self.request.user
    
    def update(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle PUT request for user profile update."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def __str__(self):
        """Return the string representation of the user."""
        return f'{self.first_name} {self.last_name}'
        # Return the updated user data
