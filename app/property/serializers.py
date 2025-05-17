""""
Serializers for the property app.
"""
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from coreapp.models import Rent, Wishlist, Contact

class PropertySerializer(serializers.ModelSerializer):
    """Serializer for the property object."""
    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('id','created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'owner': {'required': True},
            'features': {'required': True},
            'type': {'required': True},
            'contact_number': {'required': True},
            'contact_email': {'required': True},
            'category': {'required': True},
            'bedrooms': {'required': True},
            'bathrooms': {'required': True},
            'parking_spaces': {'required': False},
        }

    def create(self, validated_data):
        """Create a new property."""
        return Rent.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a property"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(update_fields=validated_data.keys())
        return instance
    
    def to_representation(self, instance):
        """Convert the property object to a dictionary."""
        representation = super().to_representation(instance)
        representation['price'] = f"${float(representation['price']):.2f}"
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        representation['updated_at'] = instance.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return representation
    
class PropertyDetailSerializer(serializers.ModelSerializer):
    """Serializer for the property detail view."""
    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields 


class WishListSerializer(serializers.ModelSerializer):
    """Serializer for the wishlsit object."""
    property = PropertySerializer(read_only=True, required=False)
    class Meta:
        model = Wishlist
        fields = ['id', 'property']
        read_only_fields = ('id',)
        extra_kwargs = {
            'property': {'required': True},
        }
    

class ContactSerializer(serializers.ModelSerializer):
    contact_number = serializers.SerializerMethodField()
    contact_email = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['rent', 'contact_number', 'contact_email','created_at', 'message']
        read_only_fields = ['contact_number', 'contact_email', 'created_at']
        extra_kwargs = {
            'rent': {'required': True},
            'created_at': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            rent = instance.rent
            representation['contact_number'] = rent.contact_number if rent else None
            representation['contact_email'] = rent.contact_email if rent else None
        except Exception as e:
            print(f"[to_representation error] {e}")
            representation['contact_number'] = None
            representation['contact_email'] = None
        return representation

    @extend_schema_field(serializers.CharField)
    def get_contact_number(self, obj):
        try:
            return obj.rent.contact_number if obj.rent else None
        except Exception as e:
            print(f"[get_contact_number error] {e}")
            return None

    @extend_schema_field(serializers.CharField)
    def get_contact_email(self, obj):
        try:
            return obj.rent.contact_email if obj.rent else None
        except Exception as e:
            print(f"[get_contact_email error] {e}")
            return None

    def create(self, validated_data):
        print("validated_data in create:", validated_data)
        return Contact.objects.create(**validated_data)

    
class ContactDetailSerializer(serializers.ModelSerializer):
    """Serializer for the contact detail view."""
    class Meta(ContactSerializer.Meta):
        fields = ContactSerializer.Meta.fields


class  RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image for property."""
    class Meta:
        model = Rent
        fields = ['id', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'image': {'required': True},
        }
    

    