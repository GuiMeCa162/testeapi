from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.parsers import MultiPartParser, FormParser
from .models import Marca, MarcaView
from .serializers import MarcaSerializer, MarcaMaisVisitadaSerializer
from roupas.serializers import ProdutoSerializer
from usuarios.permissions import IsStaffPermission
from .utils import get_client_ip


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        public_actions = {
            'list', 'retrieve', 'listar_produtos',
            'listar_recentes', 'listar_antigas',
            'listar_alfabetica', 'listar_alfabetica_desc',
            'mais_visitadas', 'top_3_produtos'
        }
        if self.action in public_actions:
            return [AllowAny()]
        return [IsStaffPermission()]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def retrieve(self, request, *args, **kwargs):
        marca = self.get_object()
        ip = get_client_ip(request)
        uma_hora_atras = timezone.now() - timedelta(hours=1)

        if not MarcaView.objects.filter(marca=marca, ip=ip, data__gte=uma_hora_atras).exists():
            MarcaView.objects.create(marca=marca, ip=ip)

        serializer = self.get_serializer(marca)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="produtos")
    def listar_produtos(self, request, pk=None):
        marca = self.get_object()
        produtos = marca.produtos.all()
        serializer = ProdutoSerializer(produtos, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="recentes")
    def listar_recentes(self, request):
        return self._listar(Marca.objects.order_by("-id_marca"))

    @action(detail=False, methods=["get"], url_path="antigas")
    def listar_antigas(self, request):
        return self._listar(Marca.objects.order_by("id_marca"))

    @action(detail=False, methods=["get"], url_path="alfabetica")
    def listar_alfabetica(self, request):
        return self._listar(Marca.objects.order_by("nome"))

    @action(detail=False, methods=["get"], url_path="alfabetica-desc")
    def listar_alfabetica_desc(self, request):
        return self._listar(Marca.objects.order_by("-nome"))

    @action(detail=False, methods=["get"], url_path="mais-visitadas")
    def mais_visitadas(self, request):
        queryset = Marca.objects.annotate(total_views=Count("views")).order_by("-total_views")[:4]
        serializer = MarcaMaisVisitadaSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def _listar(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="top-3-produtos")
    def top_3_produtos(self, request, pk=None):
        marca = self.get_object()
        produtos = marca.produtos.order_by("-n_visualizacoes")[:3]
        serializer = ProdutoSerializer(produtos, many=True, context={"request": request})
        return Response(serializer.data)

    
