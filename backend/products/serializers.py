from rest_framework import serializers
from products.models import Product
from rest_framework.reverse import reverse
from .validators import validate_title
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk')

    title = serializers.CharField(validators=[validate_title])
    # email = serializers.EmailField(write_only=True)

    class Meta:
        model = Product
        fields  = ['owner', "pk", "url", "title", "content", "price", "sale_price"]
    
    def create(self, validated_data):
        # return Product.objects.create(**validated_data)
        # email = validated_data.pop("email")
        obj = super().create(validated_data)
        print(obj)
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
    
    def get_my_user_data(self, obj):
        return {
            "username": obj.user
        }
    
    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value