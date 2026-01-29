from django.urls import path
from . import views

produto_list_create = views.ProdutoViewSet.as_view({
    "get": "list",
    "post": "create"
})
produto_detail = views.ProdutoViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy"
})

produto_tamanho_list_create = views.ProdutoTamanhoViewSet.as_view({
    "get": "list",
    "post": "create"
})
produto_tamanho_detail = views.ProdutoTamanhoViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy"
})

imagem_extra_list_create = views.ImagemExtraViewSet.as_view({
    "get": "list",
    "post": "create"
})
imagem_extra_detail = views.ImagemExtraViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy"
})

home_list = views.HomeViewSet.as_view({
    "get": "list"
})


urlpatterns = [
    # Produtos
    path("produtos/", produto_list_create, name="produto-list-create"),
    path("produtos/<int:pk>/", produto_detail, name="produto-detail"),


    # Tamanhos de Produto
    path("tamanhos-produto/", produto_tamanho_list_create, name="produto-tamanho-list-create"),
    path("tamanhos-produto/<int:pk>/", produto_tamanho_detail, name="produto-tamanho-detail"),

    # Imagens Extras
    path("imagens-extras/", imagem_extra_list_create, name="imagem-extra-list-create"),
    path("imagens-extras/<int:pk>/", imagem_extra_detail, name="imagem-extra-detail"),


    path("home/", home_list, name="home-list"),
]
