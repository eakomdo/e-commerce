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
        
        
#get a single category, update and delete        
class   CategoryDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get_object(self, slug):
        return get_object_or_404(Category, slug=slug)
    
    #get a single category
    def get(self, slug):
        Category = self.get_object(slug)
        serializer = CategorySerializer(
            Category,
            context={'request': self.request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #update a category
    def put(self, slug):
        Category = self.get_object(slug)
        serializer = CategorySerializer(
            Category,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Your category has been updated successfully'}, status=status.HTTP_200_OK)
        
    #delete a category
    def delete(self, slug):
        Category = self.get_object(slug)
        Category.delete()
        return Response({'Category deleted successfuly'}, status=status.HTTP_200_OK)
    
    
    
#product image view
class ProductImageUploadView(APIView):
    permission_classes =[IsAuthenticated]
    permission_parser = [MultiPartParser, FormParser]
    
    
    def post(self, request, slug):
        product = get_object_or_404(Product, slug)
        
        if not request.user.is_admin:
            return Response ({"You can't perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        
        #listing all images
        images = request.FILES.getlist('images')
        
        if not images:
            return Response({'No images uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        #create a product image for each image uploaded
        uploaded_images = []
        
        for index, image in enumerate(images):
            product_image = ProductImage.objects.create(product=product, images=image, order=index)
            uploaded_images.append(product_image)
            
            serializer = ProductImageSerializer(uplaoded_images, many=True, context={'request': request})
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)