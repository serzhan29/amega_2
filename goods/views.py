from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import viewsets

from goods.models import Products, Categories
from goods.utils import q_search
from goods.serializers import CategoriesSerializer, ProductsSerializer


def q_search(query):
    return Products.objects.filter(Q(name__icontains=query))


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))

    context = {
        "title": "Главная страница - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)

#====================mobile-api==============================


class MobileCategoryApi(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class ProductsCategoryApi(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer