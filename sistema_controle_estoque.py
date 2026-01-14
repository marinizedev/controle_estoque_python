import json
import os
from colorama import Fore, Back, Style, init
init(autoreset=True)
from tabulate import tabulate
import logging
DEBUG_ATIVO = True
import csv
import os

# -----------------------------
# CONFIGURAÇÃO DO ARQUIVO JSON
# -----------------------------
ARQUIVO_ESTOQUE = "estoque.json"

# ----------------------------
# CONFIGURAÇÃO DO ARQUIVO LOG
# ----------------------------
from datetime import datetime

data_atual = datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(
    filename=f"sistema_{data_atual}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ---------------------------
# FUNÇÕES DE PERSISTÊNCIA
# ---------------------------
def carregar_estoque():
    """Carrega os dados do estoque a partir do arquivo JSON."""
    if os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}
    
def salvar_estoque(estoque):
    """Salvar os dados do estoque mo arquivo JSON."""
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as arquivo:
        json.dump(estoque, arquivo, indent=4, ensure_ascii=False)

# ----------------------------
# FUNÇÕES AUXILIARES
# ----------------------------
def ler_preco_quantidade():
    """Lê e valida preço e quantidade do produto de forma segura."""
    try:

        preco_input = input(f"{COR_INPUT}Preço do produto (pressione ENTER para manter atual): ").strip()
        quantidade_input = input(f"{COR_INPUT}Quantidade em estoque (pressione ENTER para manter atual): ").strip()

        preco = float(preco_input) if preco_input else None
        quantidade = int(quantidade_input) if quantidade_input else None

        if preco is not None and preco < 0:
            print(f"{Fore.BLUE}Preço deve ser positivo.")
            return None, None
        if quantidade is not None and quantidade < 0:
            print(f"{COR_ERRO}Quantidade deve ser positiva.")
            return None, None
        return preco, quantidade
    except ValueError as erro:
        log_evento("ERROR", f"Erro ao ler preço/quantidade: {erro}")
        print(f"{COR_ERRO}Digite valores numéricos válidos.")
        return None, None
    
def buscar_produto(estoque, nome):
    """Verifica se o produto existe no estoque."""
    return estoque.get(nome)

def simular_erros():
    print(f"{COR_INPUT}\nSimulação de erros:")
    print("1 - Erro de conversão (ValuesError)")
    print("2 - Produto inexistente")
    print("3 - Erro genérico")

    opcao = input("Escolha: ").strip()

    if opcao == "1":
        try:
            int("abc")
        except ValueError as e:
            log_evento("ERROR", f"Erro simulado de conversão: {e}")
            print(f"{COR_ERRO}Erro de conversão simulado.")

    elif opcao == "2":
        nome = "ProdutoFantasma"
        log_evento("WARNING", f"Tentativa de acesso a produto inexistente: {nome}")
        print(f"{COR_ERRO}Produto inexistente simulado.")

    elif opcao == "3":
        try:
            1 / 0
        except Exception as e:
            log_evento("ERROR", f"Erro genérico simulado: {e}")
            print(f"{COR_ERRO}Erro genérico simulado.")

# --------------------------
# TEMA DE CORES DO SISTEMA
# --------------------------
TEMA_CLARO = {
    "titulo": Fore.MAGENTA,
    "menu": Fore.BLUE,
    "input": Fore.BLACK,
    "sucesso": Fore.GREEN,
    "erro": Fore.RED,
    "aviso": Fore.YELLOW
}

TEMA_ESCURO = {
    "titulo": Fore.LIGHTMAGENTA_EX,
    "menu": Fore.CYAN,
    "input": Fore.WHITE,
    "sucesso": Fore.LIGHTGREEN_EX,
    "erro": Fore.LIGHTRED_EX,
    "aviso": Fore.LIGHTYELLOW_EX
}

tema = TEMA_ESCURO

COR_TITULO = tema["titulo"]
COR_MENU = tema["menu"]
COR_INPUT = tema["input"]
COR_SUCESSO = tema["sucesso"]
COR_ERRO = tema["erro"]
COR_AVISO = tema["aviso"]

# -----------------------------
# FUNÇÃO DE APLICAÇÃO DE TEMA
# -----------------------------
def aplicar_tema(novo_tema):
    """Aplica tema do sistema"""
    global COR_TITULO, COR_MENU, COR_INPUT, COR_SUCESSO, COR_ERRO, COR_AVISO
    tema = novo_tema
    COR_TITULO = novo_tema["titulo"]
    COR_MENU = novo_tema["menu"]
    COR_INPUT = novo_tema["input"]
    COR_SUCESSO = novo_tema["sucesso"]
    COR_ERRO = novo_tema["erro"]
    COR_AVISO = novo_tema["aviso"]

# --------------------------
# FUNÇÃO CENTRAL DE LOG
# --------------------------
def log_evento(nivel, mensagem):
    """Registra eventos do sistema em log. niveis possíveis: INFO, WARNING, ERROR"""
    if not DEBUG_ATIVO:
        return
    
    if nivel == "INFO":
        logging.info(mensagem)
    elif nivel == "WARNING":
        logging.warning(mensagem)
    elif nivel == "ERROR":
        logging.error(mensagem)

# ------------------------
# MENU LIGA/DESLIGA DEBUG
# ------------------------
def alterar_debug():
    global DEBUG_ATIVO
    DEBUG_ATIVO = not DEBUG_ATIVO
    estado = "ATIVADO" if DEBUG_ATIVO else "DESATIVADO"
    print(f"{COR_SUCESSO}Modo DEBUG {estado}.")

# ----------------------
# FUNÇÕES SALVAR/CARREGAR EM CSV
# ----------------------
def salvar_estoque_csv(estoque, nome_arquivo="estoque.csv"):
    """Carregando o estoque do CSV"""
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["produto", "preco", "quantidade"]) # cabeçalho

        for produto, dados in estoque.items():
            writer.writerow([produto, dados["preco"], dados["quantidade"]])

def carregar_estoque_csv(nome_arquivo="estoque.csv"):
    estoque = {}

    if not os.path.exists(nome_arquivo):
        return estoque # se não existir, começa vazio
    
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        reader = csv.DictReader(arquivo)

        for linha in reader:
            produto = linha["produto"]
            estoque[produto] = {
                "preco":
                float(linha["preco"]),
                "quantidade":
                int(linha["quantidade"])
            }
        return estoque
    
# ------------------------
# FUNÇÕES DO SISTEMA
# ------------------------
def exibir_menu():
    """Exibe o menu de opções do sistema."""
    print(f"{COR_TITULO}\n=== SISTEMA DE CONTROLE DE ESTOQUE ===")
    print(f"{COR_MENU}1- Adicionar produto")
    print(f"{COR_MENU}2- Atualizar produto")
    print(f"{COR_MENU}3- Excluir produto")
    print(f"{COR_MENU}4- Visualizar estoque")
    print(f"{COR_MENU}5- Sair do sistema")
    print(f"{COR_MENU}6- Alterar tema")

estoque = carregar_estoque_csv()
def adicionar_produto(estoque):
    """Adiciona um produto ao estoque."""
    nome = input(f"{COR_INPUT}Nome do produto: ").strip().title()
    
    if not nome:
        print(f"{COR_ERRO}Nome inválido.")
        return
    if buscar_produto(estoque, nome):
        print(f"{COR_AVISO}Produto já existe no estoque.")
        return
        
    preco, quantidade = ler_preco_quantidade()
    log_evento("INFO", f"Produto adicionado: {nome} | Preço: {preco} | Quantidade: {quantidade}")

    if preco is None or quantidade is None:
        return # sai se os dados forem inválidos

    estoque[nome] = {
        "preco": preco,
        "quantidade": quantidade
    }
     

    salvar_estoque(estoque)
    print(f"{COR_SUCESSO}Produto adicionado com sucesso!")

def atualizar_produto(estoque):
    """Atualizar o preço e/ou quantidade um produto existente."""
    nome = input(f"{COR_INPUT}Nome do produto a atualizar: ").strip().title()
    produto = buscar_produto(estoque, nome)
      
    if produto is None:
        print(f"{COR_ERRO}Produto não encontrado.")
        log_evento("WARNING", f"Tentativa de atualizar produto inexistente: {nome}")
        return
    
    preco, quantidade = ler_preco_quantidade()

    if preco is not None :
        produto["preco"] = preco 
    if quantidade is not None:
        produto["quantidade"] = quantidade
        
    produto = buscar_produto(estoque, nome)

    salvar_estoque(estoque)
    print(f"{COR_SUCESSO}Produto atualizado com sucesso!")
    logging.info(f"Produto atualizado: {nome}")

def excluir_produto(estoque):
    """Exclui umm produto do estoque."""
    nome = input(f"{COR_INPUT}Nome do produto a excluir: ").strip().title()
    produto = buscar_produto(estoque, nome)

    if produto is None:
        print(f"{COR_ERRO}Produto não encontrado.")
        return
    
    confirmacao = input(f"{COR_INPUT}Tem certeza que deseja excluir '{nome}'? (s/n): ").strip().lower()

    if confirmacao != "s":
        print(f"{COR_SUCESSO}Exclusão cancelada.")
        return
    
    del estoque[nome]
    salvar_estoque(estoque)
    print(f"{COR_SUCESSO}Produto excluído com sucesso!")
    logging.info(f"Produto excluído: {nome}")

def visualizar_estoque(estoque):
    """Mostra todos os produtos e suas informações do estoque."""
    if not estoque:
        print(f"{COR_AVISO}Estoque vazio.")
        return
    
    tabela = []
    
    for nome, dados in estoque.items():
        tabela.append([
            nome,
            f"R$ {dados['preco']:.2f}",
            dados['quantidade']
        ])
    print(Style.RESET_ALL)
    print(tabulate(
            tabela, headers=["Produto", "Preço", "Quantidade"],
            tablefmt="grid"
        ))
    
    print(COR_INPUT + "\nPressione ENTER para continuar...")
    input()

def escolher_tema():
    print(f"{COR_INPUT}\nEscolha o tema:")
    print(f"{COR_INPUT}C - Tema Claro")
    print(f"{COR_INPUT}E - Tema Escuro")

    nome_tema = input("Opção: ").strip().upper()

    if not nome_tema:
        print(f"{COR_ERRO}Tema inválido.")
        return
    
    if nome_tema == "C":
        aplicar_tema(TEMA_CLARO)
        print(f"{COR_SUCESSO}Tema claro aplicado.")
    elif nome_tema == "E":
        aplicar_tema(TEMA_ESCURO)
        print(f"{COR_SUCESSO}Tema escuro aplicado.")
    else:
        print(f"{COR_ERRO}Opção inválida.")
    log_evento("INFO", f"Tema alterado para: {nome_tema}")        
    
    print(COR_INPUT + "\nPressione ENTER para continuar...")
    input()

# ---------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------
estoque = carregar_estoque()
aplicar_tema(TEMA_CLARO)
while True:
    exibir_menu()
    opcao = input(f"{COR_INPUT}Escolha uma opção: ")

    if opcao == "1":
        adicionar_produto(estoque)
    elif opcao == "2":
        atualizar_produto(estoque)
    elif opcao == "3":
        excluir_produto(estoque)
    elif opcao =="4":
        visualizar_estoque(estoque)
    elif opcao == "5":
        log_evento("INFO", "Sistema encerrado pelo usuário")
        print(f"{COR_AVISO}Saindo do sistema. Até logo!")
        salvar_estoque_csv(estoque)
        print("Estoque salvo com sucesso!")
        break
    elif opcao == "6":
        escolher_tema()
    else:
        print(f"{COR_ERRO}Opção inválida.")