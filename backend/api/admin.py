from django.contrib import admin
from .models import Category, Item, Tag, StockStatus

# Register Category model with admin interface
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Fields to display in the list view
    search_fields = ('name',)  # Fields to enable search functionality

# Register Item model with admin interface
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku', 'name', 'category', 'get_tags', 'stock_status', 'available_stock')  # Fields to display in the list view
    list_filter = ('category', 'stock_status')  # Filters to display in the sidebar
    search_fields = ('sku', 'name')  # Fields to enable search functionality

    # Custom method to display tags as a comma-separated list
    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Tags'  # Set short description for the custom method

# Register Tag model with admin interface
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Fields to display in the list view
    search_fields = ('name',)  # Fields to enable search functionality

# Register StockStatus model with admin interface
@admin.register(StockStatus)
class StockStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Fields to display in the list view
    search_fields = ('name',)  # Fields to enable search functionality
