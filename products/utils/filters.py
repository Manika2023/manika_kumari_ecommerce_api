# utils/filters.py
from django.db.models import Q

def apply_filters(queryset, model_name, filters):
    """
    Generic filter helper for Product and Category models.
    Supports: category_id, min_price, max_price, in_stock.
    """

    category_id = filters.get('category_id')
    min_price = filters.get('min_price')
    max_price = filters.get('max_price')
    in_stock = filters.get('in_stock')

    if model_name == 'product':
        # --- Product filtering directly ---
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if in_stock:
            if in_stock.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(stock__gt=0)
            else:
                queryset = queryset.filter(stock__lte=0)

    elif model_name == 'category':
        # --- Category filtering based on related products ---
        product_filter = Q()
        if min_price:
            product_filter &= Q(products__price__gte=min_price)
        if max_price:
            product_filter &= Q(products__price__lte=max_price)
        if in_stock:
            if in_stock.lower() in ['true', '1', 'yes']:
                product_filter &= Q(products__stock__gt=0)
            else:
                product_filter &= Q(products__stock__lte=0)
        if category_id:
            product_filter &= Q(id=category_id)

        if product_filter:
            queryset = queryset.filter(product_filter).distinct()

    return queryset
