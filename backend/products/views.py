from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title
        serializer.save(content=content, user=self.request.user)

class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk ?

class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        # instance
        super().perform_destroy(instance)


class ProductMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Como fazer tudo acima em um lugar só usando view baseado em função
@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    
    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        else:
            # lista view
            queryset = Product.objects.all()
            data = ProductSerializer(queryset, many=True).data
            return Response(data)
    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content") or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data) 
    # return Response({"invalid": "not good data"}, status=400)