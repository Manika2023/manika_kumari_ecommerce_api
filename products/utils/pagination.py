# utils/pagination.py
from django.core.paginator import Paginator

def paginate_queryset(queryset, request, serializer_class, per_page=11):
    """
    Paginate a queryset and serialize results.
    Returns a dictionary with pagination metadata and serialized data.
    """
    page_number = request.query_params.get('page', 1)
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_number)
    serializer = serializer_class(page_obj, many=True)

    return {
        "total_items": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "results": serializer.data
    }
