# Oi

Esse é um projeto do [USPCodeLab Butantã](https://codelab.ime.usp.br/)

Para instruções sobre como configurar, leia as seções abaixo.

## Estrutura

O codeclass é um web app feito com Django.

O projeto Django está em `servidor/` e o app em `servidor/ccapp`

# Configuração do Ambiente de Desenvolvimento

Este guia descreve como configurar e executar o projeto utilizando Docker Compose. O ambiente principal para rodar a aplicação é o Docker, mas também vamos configurar um ambiente virtual local para auxiliar no desenvolvimento com o seu editor de código (ex: VS Code).

## Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas:

  * **Docker e Docker Compose**: As versões mais recentes são recomendadas.
  * **uv**: O gerenciador de pacotes Python utilizado no projeto. Siga o [guia de instalação oficial](https://github.com/astral-sh/uv).

## Passo 1: Arquivo de Ambiente (`.env`)

As configurações do projeto, como as credenciais do banco de dados, são gerenciadas por um arquivo `.env`. Para começar, copie o arquivo de exemplo:

```bash
cp .env.example .env
```

> Para o ambiente de desenvolvimento local, os valores padrão no arquivo já devem funcionar.

## Passo 2: Ambiente de Desenvolvimento com Docker

O Docker é a forma principal de rodar a aplicação, garantindo um ambiente consistente e isolado.

### Iniciando os Contêineres

Na raiz do projeto, execute o comando abaixo para construir as imagens e iniciar os contêineres.

```bash
docker compose up --build
```

  * **Dica:** Adicione a flag `-d` (`docker compose up --build -d`) para rodar os contêineres em segundo plano e liberar seu terminal.

Após a execução, a aplicação Django estará disponível no seu navegador em `http://localhost:8000`.

### Executando Comandos no Contêiner

Para executar comandos dentro do contêiner da aplicação (como os comandos do `manage.py`), utilize o `docker compose exec`. O nome do nosso serviço é `django-web`.

**Exemplo:** Abrir um shell dentro do contêiner.

```bash
docker compose exec django-web bash
```

### Comandos Comuns (Banco de Dados)

Logo após iniciar o ambiente pela primeira vez, você precisará aplicar as migrações do banco de dados e criar um superusuário.

1.  **Aplicar as migrações:**

    ```bash
    docker compose exec django-web python manage.py migrate
    ```

2.  **Criar um usuário administrador:**

    ```bash
    docker compose exec -it django-web python manage.py createsuperuser
    ```

## Passo 3: Ambiente Virtual Local (Para o Editor de Código)

Apesar da aplicação rodar no Docker, é muito útil ter um ambiente virtual local. Isso permite que o seu editor de código (como o VS Code) identifique as bibliotecas instaladas para oferecer autocompletar, verificação de tipos (`type hints`) e outras funcionalidades.

**Instale as dependências com `uv`:**
    Este comando irá ler o arquivo `uv.lock` e instalar exatamente as mesmas dependências que estão no Docker, garantindo consistência.
    Também, criará um ambiente virtual chamado `.venv` na raiz do projeto.

    ```bash
    uv sync
    ```

Agora seu ambiente local está sincronizado com o do projeto\!

### Integrando com o VS Code

Para que o VS Code utilize este ambiente virtual:

1.  Abra o projeto no VS Code.
2.  Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac) para abrir a paleta de comandos.
3.  Digite e selecione **"Python: Select Interpreter"**.
4.  Escolha o interpretador Python que aponta para o seu ambiente recém-criado (`./.venv/bin/python`).

Com isso, o VS Code terá total conhecimento das bibliotecas do projeto, melhorando sua experiência de desenvolvimento.
