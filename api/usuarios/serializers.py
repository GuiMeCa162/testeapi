from rest_framework import serializers
from .models import Usuario
from django.contrib.auth import authenticate

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'tipo']
        read_only_fields = ['tipo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Criar nova instância do objeto de acordo com os dados validados.
        """
        password = validated_data.pop('password', None)
        return Usuario.objects.create_user(password=password, **validated_data)
    
    def update(self, instance, validated_data):
        """
        Atualizar instância existente de acordo com os dados validados.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class LoginUsuarioSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciais incorretas!")