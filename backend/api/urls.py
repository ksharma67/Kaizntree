from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import login_view, UserViewSet, ItemViewSet, CategoryViewSet, TagViewSet, StockStatusViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')  # Register ItemViewSet with 'items' endpoint
router.register(r'categories', CategoryViewSet, basename='category')  # Register CategoryViewSet with 'categories' endpoint
router.register(r'tags', TagViewSet, basename='tag')  # Register TagViewSet with 'tags' endpoint
router.register(r'stock-statuses', StockStatusViewSet, basename='stockstatus')  # Register StockStatusViewSet with 'stock-statuses' endpoint
router.register(r'users', UserViewSet, basename='user')  # Register UserViewSet with 'users' endpoint

# Define the urlpatterns to include router-generated URLs
urlpatterns = [
    path('', include(router.urls)),  # Include URLs generated by the router
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),  # Endpoint for user registration
    path('login/', login_view, name='login'),  # Endpoint for user login
]
