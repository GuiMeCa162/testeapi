# Backend-VitriNEPP

API para o site de exposição de roupas do VitriNEPP.  

## Install requirements

```linha de comando
pip install -r requirements.txt
```

Se o acima não funcionar (aconteceu cmg), cria um ambiente virtual pra baixar que dá certo

```linha de comando
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Banco de dados

Execute esse comando pra criar o banco de dados ou atualizá-lo se necessário

```linha de comando
python manage.py migrate
```

Para popular o banco com dados predefinidos execute o seguinte comando

```linha de comando
python manage.py loaddata db_template.json
```

## Como Rodar a API

```linha de comando
  cd api
  python manage.py runserver
```

## Endpoints

### [Markdown para Marcas](markdown/marcas.md)

### [Markdown para Roupas](markdown/roupas.md)

### [Markdown para Usuários](markdown/usuarios.md)
