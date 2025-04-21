""""
Serializers for the property app.
"""
from rest_framework import serializers
from core.models import Property, Wishlist

class PropertySerializer(serializers.ModelSerializer):
    """Serializer for the property object."""
    class Meta:
        model = Property
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
        return Property.objects.create(**validated_data)
    
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
    property = PropertySerializer
    class Meta:
        model = Wishlist
        fields = ['id', 'property']
        read_only_fields = ('id')
        extra_kwargs = {
            'property': {'required': True},
        }
