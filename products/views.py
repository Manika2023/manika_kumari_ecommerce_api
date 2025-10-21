from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from .utils.pagination import paginate_queryset
from .utils.filters import apply_filters
# import django_redis
from django.core.cache import cache
from .utils.cahce_utils import clear_cache_by_prefix

# *****************Views for Category************

# View for listing categories (anyone can view)
class CategoryListApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key_name = "categories_list"
        categories = cache.get(cache_key_name)
        if not categories:
           # Fetch from DB using optimized query
           categories = Category.objects.all()
           serializer = CategorySerializer(categories, many=True)
           cache.set(cache_key_name,serializer.data,timeout=3600)
        else:
            # fetch from cache
            serializer_data = categories
            return Response({"data":serializer_data,"message":"fetch from the cache"},status=status.HTTP_200_OK)

        return Response({
            "data": serializer.data,
            "message":"fetch from the DB"
        }, status=status.HTTP_200_OK)


class CategoryDetailApi(APIView):
        permission_classes = [AllowAny]
        def get(self,request,pk):
                # fetch from the db
                category = Category.objects.get(pk=pk)
                if not category:
                    return Response({"message":"Category is not found"},status=status.HTTP_200_OK)    
                serializer = CategorySerializer(category)
                return Response({"data":serializer.data,"message":"Category found"},status=status.HTTP_200_OK)  


# View for adding category (only admin can do)
class CategoryCreateApi(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            # Invalidate cache
            cache.delete("categories_list")  
            return Response({
                'category': CategorySerializer(category, context={'request': request}).data,
                "message": "created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "data is invalid or category name already created",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# View for updating category (only admin can do)
class CategoryUpdateApi(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        category = Category.objects.get(pk=pk)
        if not category:
            return Response({"message":"Category not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            category = serializer.save()
            cache.delete("categories_list")
            return Response({
                "message": "category updated successfully",
                "category": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "update failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# View for deleting category (only admin can do)
class CategoryDeleteApi(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        if not category:
            return Response({"message":"Category not found"},status=status.HTTP_404_NOT_FOUND)
        category.delete()
        cache.delete("categories_list")
        return Response({
            "message": "category deleted successfully"
        }, status=status.HTTP_200_OK)


# *****************Views for Product************

class ProductListApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # --- Collect filter params ---
        filters = {
            'category_id': request.query_params.get('category'),
            'min_price': request.query_params.get('min_price'),
            'max_price': request.query_params.get('max_price'),
            'in_stock': request.query_params.get('in_stock'),
        }

        # --- Unique cache key ---
        cache_key = f"products_{filters}_{request.query_params.get('page', 1)}"
        # cache_key = "products_list"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response({"message":"fetched cached data","data":cached_data}, status=status.HTTP_200_OK)

        # --- Base queryset ---
        products = Product.objects.select_related("category").all()

        # --- Apply filters using helper ---
        products = apply_filters(products, 'product', filters)

        # --- Pagination ---
        paginated_data = paginate_queryset(products, request, ProductSerializer, per_page=10)

        response_data = {
            "message": "products fetched successfully",
            **paginated_data
        }

        cache.set(cache_key, response_data, timeout=3600)
        return Response(response_data, status=status.HTTP_200_OK)
    

class ProductDetailApi(APIView):
    permission_classes = [AllowAny]   

    def get(self,request,pk):
            product = Product.objects.get(pk=pk) 
            if not product:
                return Response({"message":"product id is not found"},status=status.HTTP_404_NOT_FOUND)
            serailizer = ProductSerializer(product)    
            return Response({"message":"product found","data":serailizer.data},status=status.HTTP_200_OK)
       

# View for adding product (only admin can do)
class ProductCreateApi(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            # Invalidate all product caches
            clear_cache_by_prefix("products_")
            return Response({
                'product': ProductSerializer(product, context={'request': request}).data,
                "message": "created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "product not created. Try again!!",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# View for updating product (only admin can do)
class ProductUpdateApi(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        product = Product.objects.get(pk=pk)
        if not product:
            return Response({"message":"product is not found"})
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            # Invalidate all product caches
            clear_cache_by_prefix("products_")
            return Response({
                "message": "Updated successfully",
                "product": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "updatation not saved. Try again!!",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# View for deleting product (only admin can do)
class ProductDeleteApi(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        if not product:
            return Response({"message":"product not found"})
        product.delete()
        # Invalidate all product caches
        clear_cache_by_prefix("products_")
        return Response({
            "message": "product deleted successfully"
        }, status=status.HTTP_200_OK)


