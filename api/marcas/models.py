from django.db import models
# Create your models here.

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to="marcas/", blank=True, null=True)
    banner = models.ImageField(upload_to="marcas/", blank=True, null=True)
    email = models.CharField(max_length=100, default="email@default.com")
    telefone = models.CharField(max_length=100, default="000000000")
    

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['id_marca']
    

class MarcaView(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="views")
    ip = models.GenericIPAddressField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marca.nome} - {self.ip}"
    
    class Meta:
        indexes = [
            models.Index(fields=['marca', 'ip', 'data']),
            models.Index(fields=['marca', 'data']),
        ]
