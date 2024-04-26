from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Item, Category, Tag, StockStatus

class ItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.stock_status = StockStatus.objects.create(name='In Stock')
        self.tag = Tag.objects.create(name='Test Tag')

    def test_create_item(self):
        payload = {
            'sku': 'TEST001',
            'name': 'Test Item',
            'category': self.category.id,
            'tags': [self.tag.id],
            'stock_status': self.stock_status.id,
            'available_stock': 10
        }
        response = self.client.post(reverse('item-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Electronics', user=self.user)

    def test_model_can_create_a_category(self):
        """Check the category model can create a category."""
        old_count = Category.objects.count()
        Category.objects.create(name='Books', user=self.user)
        new_count = Category.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category_data = {'name': 'Electronics', 'user': self.user.id}
        self.response = self.client.post(
            reverse('category-list'),
            self.category_data,
            format="json")

    def test_api_can_create_a_category(self):
        """Test the api has category creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_categories(self):
        """Test the api can get a given category."""
        category = Category.objects.get(id=1)
        response = self.client.get(
            reverse('category-detail', kwargs={'pk': category.id}),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, category)

    def test_api_can_update_category(self):
        """Test the api can update a given category."""
        change_category = {'name': 'Something else'}
        res = self.client.put(
            reverse('category-detail', kwargs={'pk': Category.id}),
            change_category, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_category(self):
        """Test the api can delete a category."""
        category = Category.objects.get()
        response = self.client.delete(
            reverse('category-detail', kwargs={'pk': category.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        # Check that the response is 201 status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that a User object was actually created
        self.assertEqual(User.objects.count(), 1)
        # Check that a Token object was created for the user
        user = User.objects.get(username='newuser')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        # Additional checks can be made here, for example, verifying that the password is hashed
        self.assertTrue(user.check_password('testpassword123'))

    def test_user_registration_with_invalid_data(self):
        """
        Ensure user registration fails with invalid data
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'not-an-email',
            'password': 'short'
        }
        response = self.client.post(url, data, format='json')
        # Check that the response is 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that no user was created
        self.assertEqual(User.objects.count(), 0)


    # Add more test cases for other API endpoints