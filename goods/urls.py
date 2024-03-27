from django.urls import path, include
from rest_framework import routers

from goods import views

app_name = 'goods'
router = routers.DefaultRouter()
router.register(r'cat', views.MobileCategoryApi)
router.register(r'products', views.ProductsCategoryApi)

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('api/', include(router.urls)),
]


