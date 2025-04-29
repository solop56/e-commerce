from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _




class UserManager(BaseUserManager):
    """Manager for user profiles."""

    def create_user(self, email, username, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True, validators=[MinLengthValidator(3)])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='user_set',
        related_query_name='user',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='user_set',
        related_query_name='user',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Rent(models.Model):
    """Model for properties."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.CharField(max_length=255)
    features = models.TextField()
    property_type = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=254)
    category = models.CharField(max_length=100)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    parking_spaces = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Wishlist(models.Model):
    """Model for wishlist."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    property = models.ForeignKey(Rent, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist"if self.user else "Wishlist"
    
class Contact(models.Model):
    """Model for contact form."""
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Contact for {self.rent.name}"if self.rent else "General Contact"
    
    def contact_info(self):
        """Return the contact information for the property."""
        if self.rent:
            return {
                'contact_number': self.rent.contact_number,
                'contact_email': self.rent.contact_email
            }
        return {
            'contact_number': None,
            'contact_email': None
        }