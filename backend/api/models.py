from django.db import models
from django.contrib.auth.models import User

# Model representing a category for items
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', db_column='user_id', default=None)  # User who owns this category

# Model representing an item
class Item(models.Model):
    sku = models.CharField(max_length=20, unique=True)  # Stock Keeping Unit (SKU) for the item
    name = models.CharField(max_length=200)  # Name of the item
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')  # Category to which the item belongs
    tags = models.ManyToManyField('Tag', blank=True, related_name='items')  # Tags associated with the item
    stock_status = models.ForeignKey('StockStatus', on_delete=models.CASCADE, related_name='items')  # Stock status of the item
    available_stock = models.PositiveIntegerField(default=0)  # Available stock quantity of the item
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', default=None)  # User who owns this item

# Model representing a tag
class Tag(models.Model):
    name = models.CharField(max_length=50)  # Name of the tag
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags', default=None)  # User who owns this tag
    # Add any other relevant fields

# Model representing a stock status
class StockStatus(models.Model):
    name = models.CharField(max_length=50)  # Name of the stock status
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_statuses', default=None)  # User who owns this stock status
    # Add any other relevant fields
