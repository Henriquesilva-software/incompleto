import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ------------------------------------
#   INICIALIZAÇÃO DO BANCO DE DADOS
# ------------------------------------
def inicializar_banco():
    con = sqlite3.connect("estoque.db")
    cursor = con.cursor()

    # Criação da tabela com coluna extra (caso esteja instalando pela 1ª vez)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL,
        ultima_movimentacao TEXT
    )
    """)

    # Adiciona coluna "ultima_movimentacao" se não existir (usando uma abordagem mais robusta)
    cursor.execute("PRAGMA table_info(produtos)")
    colunas = [col[1] for col in cursor.fetchall()]

    if "ultima_movimentacao" not in colunas:
        cursor.execute("ALTER TABLE produtos ADD COLUMN ultima_movimentacao TEXT")
        con.commit()

    return con, cursor

# Função que retorna o horário atual formatado
def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ------------------------------------
#   FUNÇÕES DO SISTEMA
# ------------------------------------
def obter_input_numerico(mensagem, tipo=float):
    while True:
        try:
            return tipo(input(mensagem))
        except ValueError:
            print("Entrada inválida. Tente novamente.")

def cadastrar_produto(cursor, con):
    print("\n--- Cadastro de Produto ---")
    nome = input("Nome: ").strip()
    if not nome:
        print("Nome não pode ser vazio.\n")
        return
    categoria = input("Categoria: ").strip()
    if not categoria:
        print("Categoria não pode ser vazia.\n")
        return
    preco = obter_input_numerico("Preço: ")
    if preco <= 0:
        print("Preço deve ser positivo.\n")
        return
    quantidade = int(obter_input_numerico("Quantidade inicial: ", int))
    if quantidade < 0:
        print("Quantidade deve ser não negativa.\n")
        return

    cursor.execute("""
        INSERT INTO produtos (nome, categoria, preco, quantidade, ultima_movimentacao)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, categoria, preco, quantidade, agora()))
    con.commit()

    print("Produto cadastrado com sucesso!\n")

def excluir_produto(cursor, con):
    print("\n--- Excluir Produto ---")
    id_buscado = int(obter_input_numerico("Digite o ID do produto que deseja excluir: ", int))

    cursor.execute("SELECT nome FROM produtos WHERE id = ?", (id_buscado,))
    produto = cursor.fetchone()
    if not produto:
        print("Produto não encontrado.\n")
        return

    confirmacao = input(f"Tem certeza que deseja excluir '{produto[0]}'? (S/N): ").upper()
    if confirmacao != 'S':
        print("Exclusão cancelada.\n")
        return

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_buscado,))
    con.commit()

    print("Produto removido com sucesso!\n")

def movimentar_estoque(cursor, con):
    print("\n--- Movimentação de Estoque ---")
    id_prod = int(obter_input_numerico("ID do produto: ", int))

    cursor.execute("SELECT quantidade, nome FROM produtos WHERE id = ?", (id_prod,))
    dados = cursor.fetchone()

    if not dados:
        print("Produto não encontrado.\n")
        return

    quantidade_atual, nome = dados

    print(f"Produto: {nome} (Qtd atual: {quantidade_atual})")
    tipo = input("Entrada ou Saída? (E/S): ").upper().strip()
    if tipo not in ['E', 'S']:
        print("Tipo inválido. Use 'E' para entrada ou 'S' para saída.\n")
        return
    quantidade = int(obter_input_numerico("Quantidade: ", int))
    if quantidade <= 0:
        print("Quantidade deve ser positiva.\n")
        return

    if tipo == "S" and quantidade > quantidade_atual:
        print("Erro: estoque insuficiente.\n")
        return

    nova_qtd = quantidade_atual + quantidade if tipo == "E" else quantidade_atual - quantidade

    cursor.execute("""
        UPDATE produtos
        SET quantidade = ?, ultima_movimentacao = ?
        WHERE id = ?
    """, (nova_qtd, agora(), id_prod))

    con.commit()

    print("Movimentação registrada com sucesso!\n")

def mostrar_relatorio(cursor):
    print("\n--- Relatório de Produtos ---")

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto cadastrado.\n")
        return

    for p in produtos:
        alerta = "⚠️ ESTOQUE BAIXO!" if p[4] < 5 else ""
        ultima = p[5] if p[5] else "Sem registro"

        print(f"""
ID: {p[0]}
Nome: {p[1]}
Categoria: {p[2]}
Preço: R${p[3]:.2f}
Quantidade: {p[4]} {alerta}
Última movimentação: {ultima}
        """)

# ------------------------------------
#   PREVISÃO DE REABASTECIMENTO
# ------------------------------------
def previsao_reabastecimento(cursor):
    print("\n--- Previsão de Reabastecimento ---")
    id_prod = int(obter_input_numerico("ID do produto: ", int))

    cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (id_prod,))
    dados = cursor.fetchone()

    if not dados:
        print("Produto não encontrado.\n")
        return

    nome, quantidade = dados
    print(f"\nProduto: {nome}")
    print(f"Quantidade atual: {quantidade}")

    if quantidade == 0:
        print("Estoque zerado. Reabasteça imediatamente.\n")
        return

    consumo = obter_input_numerico("Consumo médio diário: ")
    if consumo <= 0:
        print("Consumo deve ser positivo.\n")
        return

    dias_restantes = quantidade / consumo
    data_fim = datetime.now() + timedelta(days=dias_restantes)

    print(f"\n⏳ O estoque dura aproximadamente: {dias_restantes:.1f} dias")
    print(f"📅 Estimativa de término: {data_fim.strftime('%d/%m/%Y')}\n")

# ------------------------------------
#   GRÁFICOS
# ------------------------------------
def grafico_evolucao(cursor):
    cursor.execute("SELECT id, nome, quantidade FROM produtos ORDER BY id")
    dados = cursor.fetchall()

    if not dados:
        print("Nenhum produto para exibir.\n")
        return

    ids = [str(d[0]) for d in dados]  # Usar IDs para eixo X, mais confiável
    nomes = [d[1] for d in dados]
    quantidades = [d[2] for d in dados]

    plt.figure(figsize=(10, 5))
    plt.plot(ids, quantidades, marker='o')
    plt.title("Evolução do Estoque por Produto")
    plt.xlabel("ID do Produto")
    plt.ylabel("Quantidade")
    plt.xticks(ids, [f"{id}\n{nome}" for id, nome in zip(ids, nomes)], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def grafico_categorias(cursor):
    cursor.execute("SELECT categoria, SUM(quantidade) FROM produtos GROUP BY categoria")
    dados = cursor.fetchall()

    if not dados:
        print("Nenhum dado para exibir.\n")
        return

    categorias = [d[0] for d in dados]
    quantidades = [d[1] for d in dados]

    plt.figure(figsize=(8, 5))
    plt.bar(categorias, quantidades)
    plt.title("Comparação de Estoque por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Quantidade Total")
    plt.tight_layout()
    plt.show()

def grafico_abc(cursor):
    cursor.execute("SELECT preco, quantidade FROM produtos")
    dados = cursor.fetchall()

    if not dados:
        print("Nenhum produto para exibir.\n")
        return

    valores = sorted([preco * qtd for preco, qtd in dados], reverse=True)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(valores) + 1), valores, marker='o')
    plt.title("Curva ABC de Custos de Estoque")
    plt.xlabel("Posição (ordenado por custo total)")
    plt.ylabel("Custo Total")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ------------------------------------
#   MENU DOS GRAFICOS
# ------------------------------------
def menu_Grafico_de_gestão(cursor):
    while True:
        print("""
------ Grafico de gestão ------
1 - Evolução do estoque
2 - Barras por categoria
3 - Curva ABC
4 - Voltar ao menu principal
------------------------
        """)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            grafico_evolucao(cursor)
        elif opcao == "2":
            grafico_categorias(cursor)
        elif opcao == "3":
            grafico_abc(cursor)
        elif opcao == "4":
            break
        else:
            print("Opção inválida!\n")

# ------------------------------------
#   MENU PRINCIPAL
# ------------------------------------
def menu(cursor, con):
    while True:
        print("""
========== MENU ==========
1 - Cadastrar produto
2 - Excluir produto
3 - Movimentar estoque
4 - Mostrar relatório
5 - Grafico de gestão
6 - Previsão de reabastecimento
7 - Sair
==========================
        """)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(cursor, con)
        elif opcao == "2":
            excluir_produto(cursor, con)
        elif opcao == "3":
            movimentar_estoque(cursor, con)
        elif opcao == "4":
            mostrar_relatorio(cursor)
        elif opcao == "5":
            menu_Grafico_de_gestão(cursor)
        elif opcao == "6":
            previsao_reabastecimento(cursor)
        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida!\n")

# ------------------------------------
#   EXECUÇÃO PRINCIPAL
# ------------------------------------
if __name__ == "__main__":
    con, cursor = inicializar_banco()
    try:
        menu(cursor, con)
    finally:

        con.close()
