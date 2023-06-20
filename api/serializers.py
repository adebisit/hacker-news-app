from rest_framework import serializers
from news.models import Author, Item
from pprint import pprint


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



class NewsItemsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    parent = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        model = Item
        exclude = ["item_id"]

    def validate(self, data):
        if data.get("category") == "comment":
            parent_id = data.get("parent")
            if parent_id is None:
                raise serializers.ValidationError('Comments must have a parent')
            
            try:
                data["parent"] = Item.objects.get(id=parent_id)
            except Item.DoesNotExist:
                raise serializers.ValidationError(f'Parent {parent_id} does not exist')
            
        data["is_admin"] = True
        return data
