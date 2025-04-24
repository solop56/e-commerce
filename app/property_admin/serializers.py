"""
Serializer for Admin Page
"""
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for the admin user object."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'confirm_password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},    
        }
    def validate(self, attrs):
        """Validate the user data."""
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(
                {'password': _('Passwords do not match.')},
                code='password_mismatch'
            )
        return attrs
    
    def create(self,validated_data):
        """Create a new admin User"""
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
        user.is_staff = True
        user.is_superuser = True

        # Clear any cached user data
        cache.delete(f'user_{user.id}')
        
        return user
    
    def update(self, instance, validated_data):
        """Update a user."""
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Clear any cached user data
        cache.delete(f'user_{instance.id}')
        
        return instance
    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication."""
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate the user credentials."""
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                {'detail': _('Must include "email" and "password".')},
                code='invalid_credentials'
            )

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                {'detail': _('Unable to log in with provided credentials.')},
                code='invalid_credentials'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                {'detail': _('User account is disabled.')},
                code='authorization'
            )
        attrs['user'] = user

        if not user.is_staff:
            raise serializers.ValidationError(
                {'detail': _('User is not an admin.')},
                code='authorization'
            )
        return attrs
    
    

    def save(self, **kwargs):
        """Save the user instance."""
        user = self.validated_data['user']

        return {'user': user}
    
    def to_representation(self, instance):
        """Return the user data(instance to a dictionary)"""
        data = super().to_representation(instance)
        user = instance.get('user')
        if user:
            data['user'] = AdminUserSerializer(user).data
        return data
    
    def __str__(self):
        """Return the string representation of the user."""
        return self.full_name
    

class LogOutSerializer(serializers.Serializer):
    """Serializer for user logout."""
    refresh = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'text'},
    )