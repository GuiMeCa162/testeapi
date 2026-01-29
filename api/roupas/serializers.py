from rest_framework import serializers
from decimal import Decimal, InvalidOperation
from .models import Produto, ImagemExtra, ProdutoTamanho
import json
import re


class ProdutoTamanhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoTamanho
        fields = ["id", "nome"]


class ImagemExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemExtra
        fields = ["id", "caminho"]


class ProdutoSerializer(serializers.ModelSerializer):
    tamanhos = ProdutoTamanhoSerializer(many=True, required=False)
    extraImgs = ImagemExtraSerializer(many=True, required=False)
    marca_nome = serializers.CharField(source="marca.nome", read_only=True)
    marca_email = serializers.CharField(source="marca.email", read_only=True)
    marca_telefone = serializers.CharField(source="marca.telefone", read_only=True)
    lista_imagens = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            "id",
            "nome",
            "descricao",
            "preco",
            "destaque",
            "img",
            "marca",
            "marca_nome",
            "marca_email",
            "marca_telefone",
            "extraImgs",
            "tamanhos",
            "n_visualizacoes",
            "lista_imagens",
            "genero"
        ]
    def to_internal_value(self, data):
        data = data.copy()
        if "destaque" in data:
            destaque_val = data["destaque"]
            if isinstance(destaque_val, str):
                data["destaque"] = destaque_val.lower() == "true"

        preco = data.get("preco")
        if preco is not None:
            if isinstance(preco, str):
                preco_limpo = re.sub(r"\.", "", preco)
                preco_limpo = preco_limpo.replace(",", ".")
                try:
                    data["preco"] = Decimal(preco_limpo)
                except InvalidOperation:
                    raise serializers.ValidationError({"preco": "Formato de preço inválido."})
            elif isinstance(preco, (float, int, Decimal)):
                data["preco"] = Decimal(str(preco))

        return super().to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        preco = rep.get("preco")
        if preco is not None:
            try:
                preco_decimal = Decimal(str(preco))
                rep["preco"] = f"{preco_decimal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except Exception:
                pass

        return rep

    def get_lista_imagens(self, obj):
        request = self.context.get("request")
        imagens = []

        if obj.img:
            url = obj.img.url if hasattr(obj.img, "url") else obj.img
            if request:
                url = request.build_absolute_uri(url)
            imagens.append(url)

        for extra in obj.extraImgs.all():
            if extra.caminho:
                url = extra.caminho.url if hasattr(extra.caminho, "url") else extra.caminho
                if request:
                    url = request.build_absolute_uri(url)
                imagens.append(url)

        return imagens

    def create(self, validated_data):
        request = self.context.get("request")
        produto = Produto.objects.create(**validated_data)

        tamanhos_raw = request.POST.get("tamanhos")
        if tamanhos_raw:
            try:
                tamanhos = json.loads(tamanhos_raw) 
                for t in tamanhos:
                    if isinstance(t, dict) and "nome" in t:
                        ProdutoTamanho.objects.create(produto=produto, nome=t["nome"])
                    elif isinstance(t, str):
                        ProdutoTamanho.objects.create(produto=produto, nome=t)
            except Exception:
                pass

        imagens = request.FILES.getlist("extraImgs")
        if not imagens and "extraImgs" in request.FILES:
            imagens = [request.FILES["extraImgs"]]

        for img in imagens:
            ImagemExtra.objects.create(produto=produto, caminho=img)

        return produto

    def update(self, instance, validated_data):
        request = self.context.get("request")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        tamanhos_raw = request.POST.get("tamanhos")
        if tamanhos_raw:
            instance.tamanhos.all().delete()
            try:
                tamanhos = json.loads(tamanhos_raw)
                for t in tamanhos:
                    if isinstance(t, dict) and "nome" in t:
                        ProdutoTamanho.objects.create(produto=instance, nome=t["nome"])
                    elif isinstance(t, str):
                        ProdutoTamanho.objects.create(produto=instance, nome=t)
            except Exception:
                pass

        imagens = request.FILES.getlist("extraImgs")
        if not imagens and "extraImgs" in request.FILES:
            imagens = [request.FILES["extraImgs"]]

        if imagens:
            instance.extraImgs.all().delete()
            for img in imagens:
                ImagemExtra.objects.create(produto=instance, caminho=img)

        return instance