from rest_framework import serializers
from .mongo import categories, locations, get_category_by_id, get_location_by_id


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


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        result = categories.insert_one(validated_data)
        return categories.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        categories.update_one({'_id': instance['_id']}, {'$set': validated_data})
        return categories.find_one({'_id': instance['_id']})

    def to_representation(self, instance):
        return {'id': str(instance['_id']), 'name': instance['name']}


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        result = locations.insert_one(validated_data)
        return locations.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        locations.update_one({'_id': instance['_id']}, {'$set': validated_data})
        return locations.find_one({'_id': instance['_id']})

    def to_representation(self, instance):
        return {'id': str(instance['_id']), 'name': instance['name']}


class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, validators=[validate_name])
    description = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.IntegerField(default=0, validators=[validate_quantity])
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    category_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    location_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        location_id = validated_data.pop('location_id', None)
        validated_data['category_id'] = category_id
        validated_data['location_id'] = location_id
        from .mongo import create_item
        return create_item(validated_data)

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        location_id = validated_data.pop('location_id', None)
        validated_data['category_id'] = category_id
        validated_data['location_id'] = location_id
        from .mongo import update_item
        return update_item(instance['id'], validated_data)

    def to_representation(self, instance):
        from .mongo import serialize_item
        return serialize_item(instance)

    def validate_category_id(self, value):
        if not value:
            return None
        category = get_category_by_id(value)
        if category is None:
            raise serializers.ValidationError('La categoría no existe.')
        return value

    def validate_location_id(self, value):
        if not value:
            return None
        location = get_location_by_id(value)
        if location is None:
            raise serializers.ValidationError('La ubicación no existe.')
        return value
