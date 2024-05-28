
from rest_framework import serializers
from .models import CartItem , Cart
from products.models import Product, Variation

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    variations = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'variations', 'quantity']

    def create(self, validated_data):
        request = self.context.get('request')
        product_id = validated_data.pop('product_id')
        variation_ids = validated_data.pop('variations', [])
        quantity = validated_data.get('quantity', 1)

        product = Product.objects.get(id=product_id)
        user = request.user if request.user.is_authenticated else None

        cart = None
        if user:
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                user=user,
                defaults={'quantity': quantity}
            )
        else:
            cart_id = request.session.session_key
            if not cart_id:
                request.session.create()
                cart_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(cart_id=cart_id)
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                cart=cart,
                defaults={'quantity': quantity}
            )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        if variation_ids:
            cart_item.variations.clear()
            for var_id in variation_ids:
                try:
                    variation = Variation.objects.get(id=var_id, product=product, is_active=True)
                    cart_item.variations.add(variation)
                except Variation.DoesNotExist:
                    raise serializers.ValidationError(f"Variation ID {var_id} does not exist or is inactive.")

        cart_item.save()
        return cart_item