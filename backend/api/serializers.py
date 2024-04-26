from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Item, Category, Tag, StockStatus

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        # Create user instance with hashed password
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update user instance
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'user'] 

# Serializer for Tag model
class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ['id', 'name', 'user']

# Serializer for StockStatus model
class StockStatusSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = StockStatus
        fields = ['id', 'name', 'user']

# Serializer for Item model
class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.none())
    stock_status = serializers.PrimaryKeyRelatedField(queryset=StockStatus.objects.none())

    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'category', 'tags', 'stock_status', 'available_stock']

    def __init__(self, *args, **kwargs):
        super(ItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # Set queryset for category, tags, and stock_status fields based on the authenticated user
            self.fields['category'].queryset = self.get_cached_categories(request.user)
            self.fields['tags'].queryset = self.get_cached_tags(request.user)
            self.fields['stock_status'].queryset = self.get_cached_stock_statuses(request.user)

    def get_cached_categories(self, user):
        # Retrieve or cache categories for a user
        cache_key = f"categories_{user.id}"
        categories = cache.get(cache_key)
        if not categories:
            categories = list(Category.objects.filter(user=user))
            cache.set(cache_key, categories)
        return categories

    def get_cached_tags(self, user):
        # Retrieve or cache tags for a user
        cache_key = f"tags_{user.id}"
        tags = cache.get(cache_key)
        if not tags:
            tags = list(Tag.objects.filter(user=user))
            cache.set(cache_key, tags)
        return tags

    def get_cached_stock_statuses(self, user):
        # Retrieve or cache stock statuses for a user
        cache_key = f"stock_statuses_{user.id}"
        stock_statuses = cache.get(cache_key)
        if not stock_statuses:
            stock_statuses = list(StockStatus.objects.filter(user=user))
            cache.set(cache_key, stock_statuses)
        return stock_statuses

# Serializer for creating Category instances
class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['name', 'user']

    def create(self, validated_data):
        # Create Category instance and clear cached categories
        category = Category.objects.create(**validated_data)
        cache_key = f"categories_{validated_data['user'].id}"
        cache.delete(cache_key)
        return category

# Serializer for creating Tag instances
class TagCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ['name', 'user']

    def create(self, validated_data):
        # Create Tag instance and clear cached tags
        tag = Tag.objects.create(**validated_data)
        cache_key = f"tags_{validated_data['user'].id}"
        cache.delete(cache_key)
        return tag

# Serializer for creating StockStatus instances
class StockStatusCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = StockStatus
        fields = ['name', 'user']

    def create(self, validated_data):
        # Create StockStatus instance and clear cached stock statuses
        stock_status = StockStatus.objects.create(**validated_data)
        cache_key = f"stock_statuses_{validated_data['user'].id}"
        cache.delete(cache_key)
        return stock_status

# Serializer for creating Item instances
class ItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    stock_status = serializers.PrimaryKeyRelatedField(queryset=StockStatus.objects.all())

    class Meta:
        model = Item
        fields = ['sku', 'name', 'category', 'tags', 'stock_status', 'available_stock', 'user']

    def create(self, validated_data):
        # Create Item instance and clear cached categories, tags, and stock statuses
        item = Item.objects.create(**validated_data)
        cache.delete(f"categories_{validated_data['user'].id}")
        cache.delete(f"tags_{validated_data['user'].id}")
        cache.delete(f"stock_statuses_{validated_data['user'].id}")
        return item
