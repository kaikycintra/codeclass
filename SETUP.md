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