
from rest_framework import serializers
from .models import CartItem , Cart
from products.models import Product, Variation
from products.serializer import ProductImagesSerializer
from django.db import transaction



class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    variations = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'variations', 'quantity']

    def create(self, validated_data):
        request = self.context.get('request')
        product_id = validated_data.pop('product_id')
        variation_values = validated_data.pop('variations', [])
        quantity = validated_data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with id {product_id} does not exist.")

        user = request.user if request.user.is_authenticated else None

        cart_items = None
        cart = None
        if user:
            cart_items = CartItem.objects.filter(product=product, user=user)
        else:
            cart_id = request.session.session_key
            if not cart_id:
                request.session.create()
                cart_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(cart_id=cart_id)
            cart_items = CartItem.objects.filter(product=product, cart=cart)

        variations = []
        for var in variation_values:
            category = var.get('category')
            value = var.get('value')
            try:
                variation = Variation.objects.get(
                    product=product, 
                    variation_category=category, 
                    variation_value=value, 
                    is_active=True
                )
                variations.append(variation)
            except Variation.DoesNotExist:
                raise serializers.ValidationError(f"Variation {category}: {value} does not exist or is inactive for this product.")

        with transaction.atomic():
            for cart_item in cart_items:
                existing_variations = list(cart_item.variations.all())
                if set(existing_variations) == set(variations):
                    cart_item.quantity += quantity
                    cart_item.save()
                    return self.return_cart(cart if cart else user)

            cart_item = CartItem.objects.create(
                product=product,
                quantity=quantity,
                user=user if user else None,
                cart=cart if not user else None
            )

            if variations:
                cart_item.variations.set(variations)

            cart_item.save()

        return self.return_cart(cart if cart else user)

    def return_cart(self, cart_or_user):
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

        if isinstance(cart_or_user, Cart):
            cart_items = CartItem.objects.filter(cart=cart_or_user, is_active=True)
        else:  # it's a User
            cart_items = CartItem.objects.filter(user=cart_or_user, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

        serializer = CartItemsSerializer(cart_items, many=True, context={'request': self.context.get('request')})

        data = {
            'total': total,
            'quantity': quantity,
            'cart_items': serializer.data,
            'tax': tax,
            'grand_total': grand_total
        }

        return data


        return data
    
class CartItemDecrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity']

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['variation_category', 'variation_value']

class ProductSerializer(serializers.ModelSerializer):
    product_image = ProductImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price' ,'product_image' , 'image']


class CartItemsSerializer(serializers.ModelSerializer):
    variations = VariationSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product','variations', 'quantity', 'is_active']