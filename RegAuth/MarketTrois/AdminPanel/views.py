from .models import User, Product, Category
from .serializers import UserSerializer, ProductSerializer, CategorySerializer
from rest_framework import generics


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class SomeModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        pk = self.kwargs[self.lookup_url_kwarg] ## first get value the url parameter(pk)

        ### then here convert its type to int if it an integer,
        ### it not a bad thing, path() will have done this if we specify its type 'int' in the url

        try:
            self.kwargs[self.lookup_url_kwarg] = int(pk)
            self.lookup_field = 'id' ### change the lookup field to 'id' if it an integer
        except:
            self.lookup_field = 'nom' ### change the lookup field to 'name' if it a str

        return super(SomeModelDetailView, self).get_object() ## finally call the super get_object


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SingleProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
