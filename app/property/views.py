"""
Views for the property app.
"""
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.models import Property, Wishlist
from property import  serializers


class PropertyViewSet(mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """ Views set to create, update and destroy properties"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = serializers.PropertyDetailSerializer
    queryset = Property.objects.all()


    def perform_create(self, serializer):
        """Create a new property."""
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_update(self, serializer):
        """Update a property."""
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PropertyListViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Views set to list and retrieve properties"""
    permission_classes = [AllowAny]
    serializer_class = serializers.PropertySerializer
    queryset = Property.objects.all()

    def get_queryset(self):
        """Get all Listings"""
        return Property.objects.all()
    
    def filter_queryset(self, queryset):
        """filter the queryset by id"""
        property_id = self.request.query_params.get('id')
        if property_id:
            queryset = queryset.filter(id=property_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search for properties"""
        query = request.query_params.get('query', None)
        if query:
            properties = Property.objects.filter(name__icontains=query)
        else:
            properties = Property.objects.all()
        
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WishlistViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.RetrieveModelMixin,):
    permission_classes = [IsAuthenticated]
    serializers_class = serializers.WishListSerializer
    
    def get_queryset(self):
        """Get all wishlist items for the current user"""
        return Wishlist.objects.filter(user=self.request.user)
    
    def list(self, request):
        """List all wishlist items for the current user"""
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishListSerializer(wishlist, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Add a property to the wishlist"""
        property_id = request.data.get("property_id")
        try:
            property_obj = Property.objects.get(pk=property_id)
        except Property.DoesNotExist:
            return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, property=property_obj)
        if created:
            serializer = serializers.WishListSerializer(wishlist_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Item already in wishlist."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Remove item from wishlist"""
        try:
            wishlist_item = Wishlist.objects.get(pk=pk, user=request.user)
        except Wishlist.DoesNotExist:
            return Response({"detail": "Item not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        