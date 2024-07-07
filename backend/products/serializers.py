from rest_framework import serializers
from products.models import Product
from rest_framework.reverse import reverse
from .validators import validate_title
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk')

    title = serializers.CharField(validators=[validate_title])

    class Meta:
        model = Product
        fields  = ['owner', "pk", "url", "title", "content", "price", "sale_price"]
    
    def create(self, validated_data):
        obj = super().create(validated_data)
        print(obj)
        return obj
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        return instance
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("", kwargs={"pk": obj.pk} , request=request)