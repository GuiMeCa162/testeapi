from django.db import models
from django.utils import timezone


class Produto(models.Model):
    GENERO_CHOICES = [
        ("masculino", "Masculino"),
        ("feminino", "Feminino"),
        ("unissex", "Unissex"),
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino"),
        ("Unissex", "Unissex")
    ]
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(decimal_places=2, max_digits=9)
    img = models.ImageField(upload_to="produtos/", blank=True, null=True)
    destaque = models.BooleanField(default=False)
    data_destaque = models.DateTimeField(blank=True, null=True)
    n_visualizacoes = models.IntegerField(default=0)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default="unissex")
    marca = models.ForeignKey("marcas.Marca", on_delete=models.CASCADE, related_name="produtos")

    def save(self, *args, **kwargs):
        if self.destaque and not self.data_destaque:
            self.data_destaque = timezone.now()
        super().save(*args, **kwargs)

        destaques = Produto.objects.filter(destaque=True).order_by("data_destaque")
        qtd = destaques.count()

        if qtd > 2:
            for produto in destaques[:qtd-2]:
                Produto.objects.filter(pk=produto.pk).update(destaque=False, data_destaque=None)

        elif qtd < 2:
            faltando = 2 - qtd
            outros = Produto.objects.filter(destaque=False).exclude(id=self.id).order_by("id")[:faltando]
            for produto in outros:
                Produto.objects.filter(pk=produto.pk).update(destaque=True, data_destaque=timezone.now())


    def __str__(self):
        return f"{self.nome} ({self.genero})"


class ProdutoTamanho(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="tamanhos")
    nome = models.CharField(max_length=20)

    class Meta:
        unique_together = ("produto", "nome")

    def __str__(self):
        return f"{self.produto.nome} - {self.nome}"


class ImagemExtra(models.Model):
    id = models.AutoField(primary_key=True)

    caminho = models.ImageField(upload_to="produtos/extras/")

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="extraImgs")

    def __str__(self):
        return f"Extra {self.id} de {self.produto.nome}"
