from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pprint import pprint
from news.models import Item
from django.db.models import Q
from datetime import datetime
from pytz import timezone
from . import serializers
from django.shortcuts import get_object_or_404


class NewsCollectionView(APIView):
    def get(self, request):
        utc = timezone("UTC")

        params = request.query_params
        keyword = params.get('keyword', '')
        before = params.get("before")
        after = params.get("after")
        category = params.get("category", "all")
        is_admin = bool(params.get("is_admin"))

        items = Item.objects.filter((Q(text__icontains=keyword) | Q(title__icontains=keyword)) & Q(is_admin=is_admin))
        if after:
            after = utc.localize(datetime.fromtimestamp(int(float(after))))
            items = items.filter(created_date__lte=after)
        if before:
            before = utc.localize(datetime.fromtimestamp(int(float(before))))
            items = items.filter(created_date__gte=before)
        if category != "all":
            items = items.filter(Q(category=category))
        
        serializer = serializers.NewsItemsSerializer(items, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = serializers.NewsItemsSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'message': 'Item created successfully'})
        else:
            return Response(serializer.errors, status=400)


class SingleNewsView(APIView):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = serializers.NewsItemsSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        if not item.is_admin:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = serializers.NewsItemsSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'message': 'Item updated successfully'})
        else:
            return Response(serializer.errors, status=400)
        

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        if not item.is_admin:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            item.delete()
            return Response({"message": "Deleted succesfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error while deleting ({str(e)})"})
        