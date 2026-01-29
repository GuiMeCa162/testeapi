# Marcas

Listar todas as marcas:  
`/marcas/ (GET)`  

retorno:

```json
  {
    "id_marca": int,
    "nome": string,
    "descricao": string,
    "foto_perfil": string,
    "banner": string,
    "email": string,
    "telefone": string
  }
```

Detalhes de uma marca:  
`/marcas/{id_marca}/ (GET)`  

retorno:

```json
{
  "id_marca": int,
  "nome": string,
  "descricao": string,
  "foto_perfil": string,
  "banner": string,
  "email": string,
  "telefone": string
}
```

Listar roupas de uma marca:  
`/marcas/{id_marca}/produtos/ (GET)`  

retorno:

```json
  {
    "id_roupa": int,
    "nome": string,
    "preco": float,
    "descricao": string,
    "destaque": boolean,
    "img": string,
    "tamanhos": [string],
    "extraImgs": [string]
  }
```

Listar marcas recentes:  
`/marcas/recentes/ (GET)`  

retorno: igual ao endpoint de listar todas as marcas, mas ordenado por id_marca decrescente.

Listar marcas antigas:  
`/marcas/antigas/ (GET)`  

retorno: igual ao endpoint de listar todas as marcas, mas ordenado por id_marca crescente.

Listar marcas em ordem alfabética:  
`/marcas/alfabetica/ (GET)`  

retorno: igual ao endpoint de listar todas as marcas, mas ordenado pelo nome (A → Z).

Listar marcas recentes:  
`/marcas/alfabetica-desc/ (GET)`  

retorno: igual ao endpoint de listar todas as marcas, mas ordenado pelo nome (Z → A).

retorno:

```json
{
  "id_marca": int,
  "nome": string,
  "descricao": string,
  "foto_perfil": string | null,
  "banner": string | null,
  "email": string,
  "telefone": string,
  "total_views": int
}
```

Listar os 3 produtos mais vistos de uma marca:  
`/marcas/{id_marca}/top-3-produtos/ (GET)`  

Listar marcas recentes:  
`/marcas/alfabetica-desc/ (GET)`  

[ADM] Criar nova marca:  
`/marcas/ (POST)`  

retorno:

```json
{
  "id_marca": int,
  "nome": string,
  "descricao": string,
  "foto_perfil": string,
  "banner": string,
  "email": string,
  "telefone": string
}
```

[ADM] Atualizar marca:  
`/marcas/{id_marca} (PUT)`  
retorno: mesmo que o endpoint de consulta de marca.

[ADM] Deletar marca:  
`/marcas/{id_marca} (DELETE)`
