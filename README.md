# Sistema de Controle de Estoque

Este projeto é um **sistema de controle de estoque em Python**, desenvolvido para gerenciamento de produtos, preços e quantidades. O sistema salva os dados em um arquivo JSON e mantém logs das operações realizadas.

---

## Tecnologias utilizadas

- Python 3.14.2
- Biblioteca:
    - [Colorama] -> para cores no terminal
    - [Tabulate] -> para exibir tabelas de forma organizada
    - [logging] -> para registrar eventos do sistema
    - [JSON] -> para persistência dos dados
    - [os] -> para dá acesso a várias funções do sistema operacional.

---

## Funcionalidades

- Adicionar produtos ao estoque
- Atualizar preço e quantidade de produtos existentes
- Excluir produtos do estoque
- Visualizar estoque em formato de tabela
- Alterar tema de cores do sistema (claro/escuro)
- Registrar logs de eventos (adicionar, atualizar, excluir, erros)
- Salvar automaticamente o estoque em JSON ao sair do sistema

> Observação: A função `simular_erros()` está presente apenas para fins de desenvolvimento e testes de logging. Não faz parte da funcionalidade principal do sistema.

---

## Como executar

Siga os passos abaixo para rodar o sistema localmente:

1. Clone este repositório ou baixe os arquivos.
2. Abra o terminal na pasta do projeto.
3. Execute o sistema: ```bash python sistema_controle_estoque.py
4. Siga as instruções no terminal para utilizar o sistema.
5. Pronto! O sistema será executado no terminal.

---

## Autora 

**Marinize Santana** – Estudante de Análise e Desenvolvimento de Sistemas Foco em: Banco de Dados, SQL, Modelagem de Dimensional, BI, Back-end