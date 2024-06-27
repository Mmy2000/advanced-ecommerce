def can_access_rosetta(user):
    # Only allow superusers or users with a specific permission
    return user.is_superadmin or  user.has_perm('products.can_translate') or user.has_perm('accounts.can_translate')