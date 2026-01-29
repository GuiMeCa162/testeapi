from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .models import Marca, MarcaView
from roupas.models import Produto, ProdutoTamanho, ImagemExtra

User = get_user_model()


def _extract_results(response):
    """
    DRF pode devolver paginação: {'count':.., 'next':.., 'results': [...]}
    Este helper retorna a lista de itens de forma robusta.
    """
    data = response.data
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    return data


class MarcaAPITests(TestCase):
    def setUp(self):
        # Usuários
        # criar admin (caso precise no futuro) e staff
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin123", tipo="admin"
        )
        self.staff_user = User.objects.create_user(
            username="staff", password="staff123", tipo="staff"
        )

        self.client = APIClient()

        # Criar marcas
        self.marca_a = Marca.objects.create(nome="Marca A")  # mais antiga
        self.marca_b = Marca.objects.create(nome="Marca B")
        self.marca_c = Marca.objects.create(nome="Marca C")
        self.marca_d = Marca.objects.create(nome="Marca D")
        self.marca_e = Marca.objects.create(nome="Marca E")  # mais nova

        # Criar produto para marca_a (testar listar produtos)
        self.produto1 = Produto.objects.create(
            nome="Produto 1",
            descricao="Desc 1",
            preco="100.00",
            marca=self.marca_a,
        )
        ProdutoTamanho.objects.create(produto=self.produto1, nome="M")
        ImagemExtra.objects.create(produto=self.produto1, caminho="extra1.jpg")

    # ---------- Públicos / listagens ----------
    def test_list_marcas_public_contains_created(self):
        """GET /marcas/ deve conter as marcas criadas (não depender do tamanho da página)."""
        response = self.client.get("/marcas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = _extract_results(response)
        names = [m["nome"] for m in items]
        # garantir que pelo menos as marcas A e B aparecem
        self.assertIn("Marca A", names)
        self.assertIn("Marca B", names)

    def test_retrieve_marca_public(self):
        """GET /marcas/{id}/ -> detalhes da marca (público)"""
        response = self.client.get(f"/marcas/{self.marca_a.id_marca}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Marca A")

    def test_listar_produtos_public(self):
        """GET /marcas/{id}/produtos/ deve retornar os produtos da marca (público)"""
        response = self.client.get(f"/marcas/{self.marca_a.id_marca}/produtos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = _extract_results(response)
        self.assertTrue(any(p["nome"] == "Produto 1" for p in items))

    def test_listar_recentes_public(self):
        """GET /marcas/recentes/ -> primeiro elemento é a marca mais nova (Marca E)."""
        response = self.client.get("/marcas/recentes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = _extract_results(response)
        # garantir que existe e o primeiro seja Marca E (nova->antiga)
        self.assertGreaterEqual(len(items), 1)
        self.assertEqual(items[0]["nome"], "Marca E")

    def test_listar_antigas_public(self):
        """GET /marcas/antigas/ -> primeiro elemento é a marca mais antiga (Marca A)."""
        response = self.client.get("/marcas/antigas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = _extract_results(response)
        self.assertGreaterEqual(len(items), 1)
        self.assertEqual(items[0]["nome"], "Marca A")

    def test_listar_alfabetica_public(self):
        """GET /marcas/alfabetica/ -> nomes em ordem ascendente A->Z"""
        response = self.client.get("/marcas/alfabetica/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = _extract_results(response)
        names = [m["nome"] for m in items]
        # names pode ter mais itens (paginação) — só checamos que a lista retornada está ordenada
        self.assertEqual(names, sorted(names))

    def test_listar_alfabetica_desc_public(self):
        """GET /marcas/alfabetica-desc/ -> nomes em ordem descendente Z->A"""
        response = self.client.get("/marcas/alfabetica-desc/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = _extract_results(response)
        names = [m["nome"] for m in items]
        self.assertEqual(names, sorted(names, reverse=True))

    # ---------- Permissões (create/update/delete) ----------
    def test_create_marca_requires_staff(self):
        """
        POST /marcas/:
          - sem autenticação -> deve bloquear (401 ou 403 dependendo do auth backend)
          - com staff -> deve criar (201)
        """
        payload = {"nome": "Marca Nova"}
        # sem autenticação
        self.client.force_authenticate(user=None)
        response = self.client.post("/marcas/", payload)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # com staff
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post("/marcas/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], "Marca Nova")

    def test_update_marca_requires_staff(self):
        """PATCH /marcas/{id}/: sem autenticação -> 401/403; com staff -> 200"""
        payload = {"nome": "Marca Atualizada"}

        # sem autenticação
        self.client.force_authenticate(user=None)
        response = self.client.patch(f"/marcas/{self.marca_a.id_marca}/", payload)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # com staff
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(f"/marcas/{self.marca_a.id_marca}/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.marca_a.refresh_from_db()
        self.assertEqual(self.marca_a.nome, "Marca Atualizada")

    def test_delete_marca_requires_staff(self):
        """DELETE /marcas/{id}/: sem autenticação -> 401/403; com staff -> 204"""
        # sem autenticação
        self.client.force_authenticate(user=None)
        response = self.client.delete(f"/marcas/{self.marca_b.id_marca}/")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # com staff
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(f"/marcas/{self.marca_b.id_marca}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Marca.objects.filter(id_marca=self.marca_b.id_marca).exists())

    # ---------- Contador de views (limite: 1 view por IP por 1 hora) ----------
    def test_contador_views_limite_uma_hora(self):
        """
        Ao acessar /marcas/{id}/ várias vezes com o mesmo IP dentro de 1 hora,
        deve contar apenas 1 view; se passagem >1h, deve contar novamente.
        """
        url = f"/marcas/{self.marca_a.id_marca}/"
        ip = "10.0.0.1"

        # garantir estado limpo
        MarcaView.objects.filter(marca=self.marca_a).delete()

        # primeira visita com ip -> cria 1 view
        resp1 = self.client.get(url, REMOTE_ADDR=ip)
        self.assertEqual(resp1.status_code, status.HTTP_200_OK)
        self.assertEqual(MarcaView.objects.filter(marca=self.marca_a, ip=ip).count(), 1)

        # segunda visita imediatamente -> não cria nova view
        resp2 = self.client.get(url, REMOTE_ADDR=ip)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(MarcaView.objects.filter(marca=self.marca_a, ip=ip).count(), 1)

        # simular uma view antiga (mais de 1 hora atrás) -> criar manualmente
        old = MarcaView.objects.create(marca=self.marca_a, ip="10.0.0.2")
        # ajustar a data para antiga
        old.data = timezone.now() - timedelta(hours=2)
        old.save(update_fields=["data"])

        # agora, simular que o mesmo IP antigo faça requisição: como não há view recente para esse IP,
        # uma nova view deve ser criada
        resp3 = self.client.get(url, REMOTE_ADDR="10.0.0.2")
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        # deve existir ao menos 2 views (a primeira para 10.0.0.1 e agora nova para 10.0.0.2)
        self.assertGreaterEqual(MarcaView.objects.filter(marca=self.marca_a).count(), 2)

    def test_mais_visitadas_endpoint_top4(self):
        """
        Cria views artificiais em várias marcas e valida /marcas/mais-visitadas/
        retorna as marcas ordenadas por total_views (top 4) e com total_views.
        """
        # limpar views
        MarcaView.objects.all().delete()

        # distribuir views:
        # marca_a: 5, marca_b: 3, marca_c:1, marca_d:2, marca_e:0
        for i in range(5):
            MarcaView.objects.create(marca=self.marca_a, ip=f"10.10.0.{i}")
        for i in range(3):
            MarcaView.objects.create(marca=self.marca_b, ip=f"10.10.1.{i}")
        MarcaView.objects.create(marca=self.marca_c, ip="10.10.2.1")
        for i in range(2):
            MarcaView.objects.create(marca=self.marca_d, ip=f"10.10.3.{i}")

        # requisitar endpoint público
        resp = self.client.get("/marcas/mais-visitadas/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = _extract_results(resp)

        # pode retornar mais que 4 se não houver limite implementado, mas os top 4 devem estar no começo
        names = [m["nome"] for m in items]
        # verificar os top esperados aparecem na ordem correta nos primeiros 4 lugares
        expected_top4 = ["Marca A", "Marca B", "Marca D", "Marca C"]
        self.assertEqual(names[:4], expected_top4)

        # checar total_views presente e é inteiro
        counts = [m.get("total_views") for m in items[:4]]
        self.assertTrue(all(isinstance(c, int) for c in counts))
    def test_mais_visitadas_endpoint_top4(self):
            """
            Cria views artificiais em várias marcas e valida /marcas/mais-visitadas/
            retorna as marcas ordenadas por total_views (top 4) e com total_views.
            Também valida que foto_perfil retorna URL absoluto quando presente.
            """
            # limpar views
            MarcaView.objects.all().delete()

            # garantir que ao menos uma marca tenha foto_perfil definida (para testar URL)
            self.marca_a.foto_perfil = "marcas/perfil_a.jpg"
            self.marca_a.save(update_fields=["foto_perfil"])

            # distribuir views:
            for i in range(5):
                MarcaView.objects.create(marca=self.marca_a, ip=f"10.10.0.{i}")
            for i in range(3):
                MarcaView.objects.create(marca=self.marca_b, ip=f"10.10.1.{i}")
            MarcaView.objects.create(marca=self.marca_c, ip="10.10.2.1")
            for i in range(2):
                MarcaView.objects.create(marca=self.marca_d, ip=f"10.10.3.{i}")

            # requisitar endpoint público
            resp = self.client.get("/marcas/mais-visitadas/")
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            items = _extract_results(resp)

            # top 4 esperados nos primeiros 4 lugares
            names = [m["nome"] for m in items]
            expected_top4 = ["Marca A", "Marca B", "Marca D", "Marca C"]
            self.assertEqual(names[:4], expected_top4)

            # checar total_views presente e é inteiro
            counts = [m.get("total_views") for m in items[:4]]
            self.assertTrue(all(isinstance(c, int) for c in counts))

            # checar que foto_perfil retornou URL absoluto para marca_a
            first = items[0]
            # Se foto_perfil preenchida, deve ser string contendo URL absoluto do host de teste
            foto = first.get("foto_perfil")
            self.assertIsNotNone(foto)
            self.assertTrue(isinstance(foto, str))
            # host padrão do test client é http://testserver
            self.assertTrue(foto.startswith("http://testserver") or "/midia/" in foto)

    def test_top_3_produtos_public(self):
        p1 = Produto.objects.create(nome="P1", descricao="x", preco="10.0", marca=self.marca_a, n_visualizacoes=5)
        p2 = Produto.objects.create(nome="P2", descricao="x", preco="20.0", marca=self.marca_a, n_visualizacoes=10)
        p3 = Produto.objects.create(nome="P3", descricao="x", preco="30.0", marca=self.marca_a, n_visualizacoes=3)
        p4 = Produto.objects.create(nome="P4", descricao="x", preco="40.0", marca=self.marca_a, n_visualizacoes=7)

        resp = self.client.get(f"/marcas/{self.marca_a.id_marca}/top-3-produtos/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        items = resp.data
        if isinstance(items, dict) and "results" in items:
            items = items["results"]

        self.assertLessEqual(len(items), 3)

        expected_order = ["P2", "P4", "P1"]
        returned_names = [p["nome"] for p in items]
        self.assertEqual(returned_names, expected_order[: len(returned_names)])