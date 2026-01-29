from rest_framework import serializers
from .models import Marca


class MarcaSerializer(serializers.ModelSerializer):


    class Meta:
        model = Marca
        fields = [
            "id_marca",
            "nome",
            "descricao",
            "foto_perfil",
            "banner",
            "email",
            "telefone",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        if request:
            if instance.foto_perfil:
                representation["foto_perfil"] = request.build_absolute_uri(instance.foto_perfil.url)
            if instance.banner:
                representation["banner"] = request.build_absolute_uri(instance.banner.url)

        return representation


class MarcaMaisVisitadaSerializer(serializers.ModelSerializer):
    total_views = serializers.IntegerField()
    foto_perfil = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()

    class Meta:
        model = Marca
        fields = [
            "id_marca",
            "nome",
            "descricao",
            "foto_perfil",
            "banner",
            "email",
            "telefone",
            "total_views",
        ]

    def _absolute_url(self, field):
        if not field:
            return None
        request = self.context.get("request", None)
        try:
            url = field.url
        except Exception:
            return None

        if request:
            return request.build_absolute_uri(url)
        return url

    def get_foto_perfil(self, obj):
        return self._absolute_url(obj.foto_perfil)

    def get_banner(self, obj):
        return self._absolute_url(obj.banner)
