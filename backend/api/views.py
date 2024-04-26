# Import necessary modules
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Item, Category, Tag, StockStatus
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, ItemSerializer, CategorySerializer, TagSerializer, StockStatusSerializer

# Define a mixin for creating model instances
class CreateModelMixin:
    def create(self, request, *args, **kwargs):
        # Retrieve serializer instance
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Associate the request user with the user field of the object
            serializer.validated_data['user'] = request.user
            # Save the serializer data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Define pagination settings
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Define viewsets for each model
class ItemViewSet(CreateModelMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

class CategoryViewSet(CreateModelMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class TagViewSet(CreateModelMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class StockStatusViewSet(CreateModelMixin, viewsets.ModelViewSet):
    queryset = StockStatus.objects.all()
    serializer_class = StockStatusSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

# Define viewset for User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Call the create method of the superclass
        response = super(UserViewSet, self).create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Retrieve the created user instance
            user = User.objects.get(username=response.data['username'])
            # Generate or retrieve token for the user
            token, created = Token.objects.get_or_create(user=user)
            # Add token to the response data
            response.data['token'] = token.key
        return response

# Define a view for user login
@api_view(['POST'])
def login_view(request):
    # Retrieve username and password from request data
    username = request.data.get('username')
    password = request.data.get('password')
    # Authenticate user
    user = authenticate(username=username, password=password)
    if user:
        # If user is authenticated, generate or retrieve token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        # If authentication fails, return error response
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
