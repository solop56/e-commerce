"""
Viewset for the admin page
"""
from typing import Any
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from core.models import User
from property_admin.serializers import AdminUserSerializer, AuthTokenSerializer, LogOutSerializer


class CreateAdminUserView(generics.CreateAPIView):
    """Create a new admin user in the system.
    
    This view handles admin user registration with the following features:
    - Validates user input using AdminUserSerializer
    - Throttles registration attempts to prevent abuse
    """
    serializer_class = AdminUserSerializer
    throttle_classes = [UserRateThrottle]

class UserAdminLoginView(TokenObtainPairView):
    """Handle admin user login and token generation."""
    serializer_class = AuthTokenSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle POST request for admin_user login."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Get the validated user
            admin = serializer.validated_data['user']
            
            # Generate tokens
            refresh = RefreshToken.for_user(admin)
            
            # Get user data using UserSerializer
            user_data = AdminUserSerializer(admin).data
            
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
    
class UserAdminLogoutView(generics.GenericAPIView):
    """Handle user logout and token blacklisting.
    
    This view allows admin users to log out by blacklisting their refresh token.
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
        
class AdminListView(generics.ListAPIView):
    """List all admin users."""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    def get_admin_stats(self, request):
        """Get admin Stat and all user"""
        total_users = User.objects.count()
        total_admins = User.objects.filter(is_staff=True).count()
        return Response({
            'total_users': total_users,
            'total_admins': total_admins
        })
    
    def list(self, request):
        """Get all users and admin details"""
        user = self.get_queryset()
        serializer = self.get_serializer(user, many=True)
        return Response(serializer.data)
    
class BanUserView(generics.UpdateAPIView):
    """Ban a user by setting their is_active field to False."""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('id'))

        user.is_active = False
        user.save()

        return Response({
            'id': user.id,
            'is_active': user.is_active,
            'detail': 'User banned successfully'
        }, status=status.HTTP_200_OK)