from rest_framework import serializers
from products.models import Product
from rest_framework.reverse import reverse

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk')

    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Product
        fields  = ["pk", "url", "email", "title", "content", "price", "sale_price", "my_discount"]
    
    def create(self, validated_data):
        # return Product.objects.create(**validated_data)
        email = validated_data.pop("email")
        obj = super().create(validated_data)
        print(email, obj)
        return obj
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        return instance
    
    def get_my_discount(self, obj):
        try:
            return obj.get_discount()
        except:
            return None
    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("", kwargs={"pk": obj.pk} , request=request)