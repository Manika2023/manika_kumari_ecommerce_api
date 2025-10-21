from django.urls import path
from products import views


urlpatterns = [
    path('category/list/', views.CategoryListApi.as_view(),name="category_list"),
    path("category/detail/<int:pk>/",views.CategoryDetailApi.as_view(),name="category_detail"),
    path('category/create/', views.CategoryCreateApi.as_view(),name="category_create"),
    path('category/update/<int:pk>/', views.CategoryUpdateApi.as_view(),name="category_update"),
    path('category/delete/<int:pk>/', views.CategoryDeleteApi.as_view(),name="category_update"),
    
    path('product/list/', views.ProductListApi.as_view(),name="product_list"),
    path("product/detail/<int:pk>/",views.ProductDetailApi.as_view(),name="product_detail"),
    path('product/create/', views.ProductCreateApi.as_view(),name="product_create"),
    path('product/update/<int:pk>/', views.ProductUpdateApi.as_view(),name="product_update"),
    path('product/delete/<int:pk>/', views.ProductDeleteApi.as_view(),name="product_delete")
]
