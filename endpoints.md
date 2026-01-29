### /roupas/

`/roupas/`

[
    {
        "id": 0,
        "nome": "",
        "preco": 0.00,
        "caminho_imagem": "",
        "descricao": "",
        "destaque": false,
        "id_marca": 0,
        "n_visualizacoes": 0,
        "n_curtidas": 0
    }
]

`/roupas/<int:pk>/`

{
    "id": 0,
    "nome": "",
    "preco": 0.00,
    "caminho_imagem": "",
    "descricao": "",
    "destaque": false,
    "id_marca": 0,
    "n_visualizacoes": 0,
    "n_curtidas": 0
}

`/roupas/descubra/`

[
    {
        "id": 0,
        "nome": "",
        "preco": 0.00,
        "caminho_imagem": "",
        "descricao": "",
        "destaque": false,
        "id_marca": 0,
        "n_visualizacoes": 0,
        "n_curtidas": 0
    }
]

`/roupas/novidades?limit=<limit>&offset=<offset>/`

[
    {
        "id": 0,
        "nome": "",
        "preco": 0.00,
        "caminho_imagem": "",
        "descricao": "",
        "destaque": false,
        "id_marca": 0,
        "n_visualizacoes": 0,
        "n_curtidas": 0
    }
]

`/roupas/populares?limit=<limit>&offset=<offset>/`

[
    {
        "id": 0,
        "nome": "",
        "preco": 0.00,
        "caminho_imagem": "",
        "descricao": "",
        "destaque": false,
        "id_marca": 0,
        "n_visualizacoes": 0,
        "n_curtidas": 0
    }
]

`/roupas/remover_destaque/<int:pk>/`
`/roupas/destacar/<int:pk>/`

### /marcas/

`/marcas/`

[
    {
        "id": 0,
        "nome": "",
        "caminho_foto": "",
        "descricao": "",
        "caminho_banner": "",
        "roupas": [
            {
                "id": 0,
                "nome": "",
                "preco": 0.00,
                "caminho_imagem": "",
                "descricao": "",
                "destaque": false,
                "id_marca": 0,
                "n_visualizacoes": 0,
                "n_curtidas": 0
            }
        ]
    }
]

`/marcas/<int:pk>/`

{
    "id": 0,
    "nome": "",
    "caminho_foto": "",
    "descricao": "",
    "caminho_banner": "",
    "roupas": [
        {
            "id": 0,
            "nome": "",
            "preco": 0.00,
            "caminho_imagem": "",
            "descricao": "",
            "destaque": false,
            "id_marca": 0,
            "n_visualizacoes": 0,
            "n_curtidas": 0
        }
    ]
}

### Parâmetros para crud
- Adicionar roupa:
```
{
    "nome": "",
    "preco": 0.00,
    "caminho_imagem": "",
    "descricao": ""
    "id_marca": 0
}
```

- Adicionar marca:
```
{
    "nome": "",
    "caminho_foto"> "",
    "descricao": "",
    "caminho_banner": ""
}
```