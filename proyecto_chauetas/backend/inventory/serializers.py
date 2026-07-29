from rest_framework import serializers
from .models import Category, Location, Item


def validate_name(value):
    if not value or not value.strip():
        raise serializers.ValidationError('El nombre es obligatorio.')
    return value


def validate_quantity(value):
    if value is None:
        return 0
    if value < 0:
        raise serializers.ValidationError('La cantidad no puede ser negativa.')
    return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'category', 'location', 'category_id', 'location_id', 'created_at']

    def validate_name(self, value):
        return validate_name(value)

    def validate_quantity(self, value):
        return validate_quantity(value)
