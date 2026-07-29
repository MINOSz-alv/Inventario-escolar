from bson import ObjectId
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ItemSerializer, CategorySerializer, LocationSerializer
from .mongo import categories, locations, items, to_object_id, get_item_by_id


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        docs = list(categories.find())
        serializer = CategorySerializer(docs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            doc = categories.find_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not doc:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(CategorySerializer(doc).data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CategorySerializer(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            instance = categories.find_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.update(instance, serializer.validated_data)
        return Response(CategorySerializer(updated).data)

    def destroy(self, request, pk=None):
        try:
            result = categories.delete_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if result.deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        docs = list(locations.find())
        serializer = LocationSerializer(docs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            doc = locations.find_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not doc:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(LocationSerializer(doc).data)

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(LocationSerializer(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            instance = locations.find_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.update(instance, serializer.validated_data)
        return Response(LocationSerializer(updated).data)

    def destroy(self, request, pk=None):
        try:
            result = locations.delete_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if result.deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        docs = list(items.find().sort('created_at', -1))
        serializer = ItemSerializer(docs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            doc = get_item_by_id(pk)
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not doc:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(doc).data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ItemSerializer(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            instance = get_item_by_id(pk)
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.update({'id': pk}, serializer.validated_data)
        return Response(ItemSerializer(updated).data)

    def destroy(self, request, pk=None):
        try:
            result = items.delete_one({'_id': to_object_id(pk)})
        except ValueError:
            return Response({'detail': 'ID inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if result.deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
