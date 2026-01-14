# Sistema de Controle de Estoque

Sistema de controle de estoque em Python. Permite adicionar, atualizar,excluir e visualizar produtos, com persistência em arquivos JSON e CSV. Possui tema claro/escuro e logging para depuração.

---

## Tecnologias utilizadas

- Python 3.14.2
- Biblioteca:
    - [Colorama] (https://pypi.org/project/colorama/) -> para cores no terminal
    - [Tabulate] (https://pypi.org/project/tabulate/) -> para exibição de tabelas
- Arquivos de persistência: JSON e CSV

---

## Funcionalidades

- Adicionar produtos (nome, preço e quantidade)
- Atualizar produtos existentes
- Excluir produtos
- Visualizar estoque em tabela
- Alterar tema (claro/escuro)
- Logging para depuração (modo DEBUG ativável/desativável)

---

## Como executar

Siga os passos abaixo para rodar o sistema localmente:

1. **Clone o repositório** ```bash git clone https://github.com/marinizedev/controle_estoque_python.git
2. **Entre na pasta do projeto** ```bash cd controle_estoque_python
3. **Instale as dependências** ```bash pip install coloroma tabulate
4. **Execute o sistema** ```bash python sistema_controle_estoque.py
5. Pronto! O sistema será executado no terminal.