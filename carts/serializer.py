
from rest_framework import serializers
from .models import CartItem , Cart
from products.models import Product, Variation



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

        product = Product.objects.get(id=product_id)
        user = request.user if request.user.is_authenticated else None

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

        # Convert variation_values to Variation instances
        variations = []
        for var in variation_values:
            category = var.get('category')
            value = var.get('value')
            try:
                variation = Variation.objects.get(product=product, variation_category=category, variation_value=value, is_active=True)
                variations.append(variation)
            except Variation.DoesNotExist:
                raise serializers.ValidationError(f"Variation {category}: {value} does not exist or is inactive for this product.")

        # Check if a cart item with the same variations already exists
        for cart_item in cart_items:
            existing_variations = list(cart_item.variations.all())
            if set(existing_variations) == set(variations):
                cart_item.quantity += quantity
                cart_item.save()
                return cart_item

        # If no matching cart item exists, create a new one
        cart_item = CartItem.objects.create(
            product=product,
            quantity=quantity,
            user=user if user else None,
            cart=cart if not user else None
        )

        if variations:
            cart_item.variations.set(variations)

        cart_item.save()
        return cart_item
    
class CartItemDecrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity']