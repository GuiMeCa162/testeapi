# Usuarios

[ADM] = Pode gerenciar roupas, marcas e dados próprios  
[SuperADM] = Tudo de ADM e gerenciar outros usuários

## [SuperADM] Criar ADM

**Endpoint:**  
`/usuarios/create/` (POST)

## [SuperADM] Listar ADMS

**Endpoint:**  
`/usuarios/list/` (GET)

## [SuperADM] Gerenciar ADM

**Endpoint:**  
`/usuarios/detail/<int:pk>/` (GET, PUT, PATCH, DELETE)

## Retornar usuário logado

**Endpoint:**  
`/usuarios/me/` (GET)

```json
{
  "username": string,
  "tipo": string,
}
```

## Tokens

`/usuarios/login/` (POST)  
Recebe as credenciais do usuário e loga ele se forem corretas, depois gera o access e o refresh token  

Recebe (precisa ter credentials: "include"):

```json
{
  "username": string,
  "password": string,
}
```

Exemplo de retorno:

```json
{
    "user": {
        "username": "Admin",
        "tipo": "admin"
    }
}
```

`/usuarios/logout/` (POST)  
Desloga o usuário e deleta o access e o refresh token  

Não recebe nada (precisa ter credentials: "include")

`/usuarios/refresh/` (POST)  
Utiliza o refresh token do usuário logado e gera um novo access token

Não recebe nada (precisa ter credentials: "include")

`api/token/` (POST)  
Valida o usuário e retorna access e refresh token  

`api/token/refresh/` (POST)  
Recebe um refresh token e devolve um novo access token  
