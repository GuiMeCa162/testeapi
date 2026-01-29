# Roupas

## [ADM] Criar Roupa

**Endpoint:**  
`POST /roupas/produtos/`

**Corpo do forms:**

```forms
{
  "nome": "nome da camiseta",
  "descricao": "descrição da roupa",
  "preco": "preco da roupa",
  "destaque": "precisa ser true pra saber se é destaque e false para negar",
  "img": "imagem pricipal da roupa",
  "marca": id da marca,
  "extraImgs": [
    {"caminho": "imagem extras da roupa"},
  ],
  "tamanhos": [
    {"nome": "tamanho da roupa"},
  ],
  "genero": "pode receber Masculino, Feminino, Unissex"
}
```

### Exemplo

```json
{
  "nome": "Camiseta Polo",
  "descricao": "Camiseta básica de algodão",
  "preco": 89.90,
  "destaque": true,
  "img": "principal.jpg",
  "marca": 1,
  "extraImgs": [
    {"caminho": "extra1.jpg"},
    {"caminho": "extra2.jpg"}
  ],
  "tamanhos": [
    {"nome": "P"},
    {"nome": "M"},
    {"nome": "G"}
  ],
  "genero": "Masculino"
}
```

## [ADM] Editar Roupas

**Endpoint:**  
`PUT /roupas/produtos/<int:pk>/`

**Corpo do forms:**

```json
{
  "nome": "Camiseta Polo",
  "descricao": "Camiseta básica de algodão",
  "preco": 89.90,
  "destaque": true,
  "img": "principal.jpg",
  "marca": 1,
  "extraImgs": [
    {"caminho": "extra1.jpg"},
    {"caminho": "extra2.jpg"}
  ],
  "tamanhos": [
    {"nome": "P"},
    {"nome": "M"},
    {"nome": "G"}
  ],
  "n_visualizacoes": 1,
  "genero": "Masculino"
}
```

## Exibir Roupa

**Endpoint:**  
`GET /roupas/produtos/<int:pk>/`

**retorna:**

```json
{
  "nome": "Camiseta Polo",
  "descricao": "Camiseta básica de algodão",
  "preco": 89.90,
  "destaque": true,
  "img": "principal.jpg",
  "marca": 1,
  "marca_nome": "nike",
  "marca_email": "marca@gmail.com",
  "marca_telefone": "84 992467426"
  "extraImgs": [
    {"caminho": "extra1.jpg"},
    {"caminho": "extra2.jpg"}
  ],
  "tamanhos": [
    {"nome": "P"},
    {"nome": "M"},
    {"nome": "G"}
  ],
  "n_visualizacoes": 1,
  "lista_imagens": [
  "principal.jpg",
  "extra1.jpg"
  "extra2.jpg"
  ],
  "genero": "Masculino"
}
```

## URL Com Paginação

1. GET /roupas/produtos/?page=1
2. GET /roupas/produtos/?destaque=&marca=&tamanhos__nome=
3. GET /roupas/produtos/?search=
4. GET /roupas/produtos/?ordering=

```obs
{
  OBS: tem que ser colocado as interrogações (?) apos a ultima barra (/)

  Eles podem ser usados todos de uma vez porem tem que ser concatenado pelo simbolo "&"
  
}
```

## URL do HOME

`GET /roupas/home/`

Sera retornado uma lista com 16 informações analogas ao item abaixo com o os dois primeiros itens sendo destaques
  
```json
[
    {
        "id": 35,
        "nome": "oi",
        "descricao": "124",
        "preco": "53.00",
        "destaque": true,
        "img": "242",
        "extraImgs": [],
        "tamanhos": [],
        "marca": 1,
        "marca_nome": "marca1",
        "marca_telefone": "84991897776",
        "marca_email": "email_marcateste1@gmail.com",
        "n_visualizacoes": 2
    },
  ]
```

## [ADM] Deletar Roupas

**Endpoint:**  
`DELETE /roupas/produtos/<int:pk>/`
