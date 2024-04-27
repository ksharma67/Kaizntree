from .admin import ItemAdmin
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from rest_framework.authtoken.models import Token
from .models import Category, Item, Tag, StockStatus
from rest_framework.test import APITestCase, APIClient
from .serializers import UserSerializer, CategorySerializer, TagSerializer, StockStatusSerializer, ItemSerializer

class MockRequest:
    pass

class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a category
        self.category = Category.objects.create(name='Electronics', user=self.user)
        
        # Create a tag
        self.tag = Tag.objects.create(name='Portable', user=self.user)
        
        # Create a stock status
        self.stock_status = StockStatus.objects.create(name='In Stock', user=self.user)
        
        # Create an item
        self.item = Item.objects.create(
            sku='123ABC',
            name='Laptop',
            category=self.category,
            stock_status=self.stock_status,
            available_stock=15,
            user=self.user
        )
        self.item.tags.add(self.tag)

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.user, self.user)

    def test_item_creation(self):
        self.assertEqual(self.item.sku, '123ABC')
        self.assertEqual(self.item.name, 'Laptop')
        self.assertEqual(self.item.category, self.category)
        self.assertTrue(self.item.tags.filter(name='Portable').exists())
        self.assertEqual(self.item.stock_status.name, 'In Stock')
        self.assertEqual(self.item.available_stock, 15)
        self.assertEqual(self.item.user, self.user)

class ItemAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(username='admin', password='password')
        self.category = Category.objects.create(name="Electronics", user=self.user)
        self.stock_status = StockStatus.objects.create(name="In Stock", user=self.user)
        self.item_admin = ItemAdmin(Item, self.site)
        self.item = Item.objects.create(
            sku="123ABC", name="Laptop", category=self.category,
            stock_status=self.stock_status, available_stock=10, user=self.user
        )

    def test_list_display(self):
        expected = ('id', 'sku', 'name', 'category', 'get_tags', 'stock_status', 'available_stock')
        self.assertEqual(self.item_admin.list_display, expected)

    def test_list_filter(self):
        expected = ('category', 'stock_status')
        self.assertEqual(self.item_admin.list_filter, expected)

    def test_search_fields(self):
        expected = ('sku', 'name')
        self.assertEqual(self.item_admin.search_fields, expected)

class SerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.category = Category.objects.create(name='Electronics', user=self.user)
    
    def test_user_serializer(self):
        # Test user creation through serializer
        user_serializer = UserSerializer(data=self.user_data)
        self.assertTrue(user_serializer.is_valid())
        
        new_user = user_serializer.save()
        self.assertEqual(new_user.username, 'testuser')
        self.assertTrue(new_user.check_password('password'))

        # Test user serialization
        serialized_user = UserSerializer(new_user).data
        self.assertEqual(serialized_user['username'], 'testuser')
        self.assertNotIn('password', serialized_user)  # Password should not be included in serialized data

    def test_category_serializer(self):
        # Test category serialization
        category_serializer = CategorySerializer(self.category)
        self.assertEqual(category_serializer.data, {
            'id': self.category.id,
            'name': 'Electronics',
            'user': self.user.id
        })

class ViewTestCase(APITestCase):
    def setUp(self):
        # Setup a user and authenticate with a token
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name="Electronics", user=self.user)
        self.item = Item.objects.create(name="Laptop", category=self.category, user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_item_viewset_list(self):
        # Test the list action of ItemViewSet
        url = reverse('item-list')  # Adjust this to match your URL name configuration
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming pagination is used

    def test_item_viewset_create(self):
        # Test the create action of ItemViewSet
        url = reverse('item-list')  # Adjust this to match your URL name configuration
        data = {
            "name": "Smartphone",
            "category": self.category.id,
            "user": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_login_view(self):
        # Test the login view
        url = reverse('login')  # Adjust this to match your URL name configuration
        data = {
            "username": "testuser",
            "password": "password"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


