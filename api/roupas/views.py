from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import F
import random
from rest_framework.decorators import action
from .models import Produto, ImagemExtra, ProdutoTamanho
from usuarios.permissions import IsStaffPermission
from .serializers import ProdutoSerializer, ImagemExtraSerializer, ProdutoTamanhoSerializer



class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["destaque", "marca", "genero", "tamanhos__nome"]
    search_fields = ["nome", "descricao", "marca__nome"]
    ordering_fields = ["preco", "n_visualizacoes", "nome", "id"]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffPermission()]
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.n_visualizacoes = F("n_visualizacoes") + 1
        instance.save(update_fields=["n_visualizacoes"])
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProdutoTamanhoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoTamanho.objects.all()
    serializer_class = ProdutoTamanhoSerializer


class ImagemExtraViewSet(viewsets.ModelViewSet):
    queryset = ImagemExtra.objects.all()
    serializer_class = ImagemExtraSerializer


class HomeViewSet(viewsets.ViewSet):
    def list(self, request):
        destaques = Produto.objects.filter(destaque="True")[:2]
        outros = list(Produto.objects.filter(destaque="False"))
        random.shuffle(outros)
        outros = outros[:14]

        serializer_destaques = ProdutoSerializer(destaques, many=True, context={"request": request})
        serializer_outros = ProdutoSerializer(outros, many=True, context={"request": request})

        return Response({
            "destaques": serializer_destaques.data,
            "outros": serializer_outros.data
        })
    

