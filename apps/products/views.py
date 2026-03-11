from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .filters import ProductFilter
from .serializers import(
    ProductSerialiser,
    CategorySerializer,
    ProductImageSerializer
)
from .models import Product, Category, ProductImage


#permission funtion
class IsAdminOrReadOnly(AllowAny):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return (request.user.is_authenticated and request.user_is_admin)
    

class CategoryListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    #list categories
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    #create a category
    def post(self, request):
        serializer = CategorySerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Category has been added successsfuly'}, status=status.HTTP_200_OK)
        