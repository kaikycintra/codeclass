# SETUP

Esse tutorial mostra como configurar o ambiente de desenvolvimento no linux.

## Ambiente virtual de python

É recomendado usar o pyenv para gerenciar múltiplas versões de python e seus pacotes:

1. Instale o pyenv seguindo as instruções no [repositório oficial](https://github.com/pyenv/pyenv).
2. Instale o python 3.12.7 com o pyenv:
    ```bash
    pyenv install 3.12.7
    ```
3. Determine a versão local:
    ```bash
    pyenv local 3.12.7
    ```
4. Crie o ambiente virtual:
    ```bash
    python -m venv .venv
    ```
5. Ative ele com:
    ```bash
    source .venv/bin/activate
    ```
6. Verifique se seu terminal começa com (.venv)
7. Verifique se não existem pacotes instalados com `pip list`
8. Apague o arquivo que determina a versão local para o pyenv
    ```bash
    rm .python-version
    ```
9. Instale os pacotes necessários
    ```bash
    pip install -r requirements.txt
    ```

### Ambiente virtual no VSCode

No VSCode, é possível ativar o ambiente automaticamente ao configurar o interpretador Python para o ambiente virtual criado. Para isso:

1. Pressione `Ctrl+Shift+P` e procure por **Python: Select Interpreter**.
2. Escolha o ambiente virtual criado na lista.

## Docker Setup

Esse projeto utiliza Docker para garantir um ambiente de desenvolvimento consistente. É necessário que tenha os seguintes pacotes em seu computador:

- **Docker versão 28.4.0** ou posterior
- **Docker compose versão 2.39.2** ou posterior

### Iniciando

Na raiz do projeto execute (opcionalmente, adicione a flag `-d` para poder continuar usando o console).

```bash
docker compose up --buid
```

Então, você pode acessar o site com a url `localhost:8000`

### Comandos

É possível executar comandos utilizando o `exec`, como:

```bash
docker-compose exec <nome_container> <comando aqui>
```

ou

```bash
docker container exec <nome_container> <comando aqui>
```

### Migrações

Caso já exista uma database no seu projeto, o Docker irá se conectar à ela por um **bind mount**. Caso ela não exista, utilize

```bash
docker container exec <nome_container> python manage.py migrate
```

e crie um usuário administrador:

```bash
docker container exec <nome_container> python manage.py createsuperuser
```
