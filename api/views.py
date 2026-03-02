from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostSerializer


#views with generics
class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerialize
    

class BlogPostUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.object.all()
    serializer_class = BlogPostSerializer