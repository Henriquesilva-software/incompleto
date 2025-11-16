import matplotlib.pyplot as plt

produtos = []
proximo_id = 1


# ----------------------------
#   CADASTRO E EXCLUSÃO
# ----------------------------
def cadastrar_produto():
    global proximo_id
    print("\n--- Cadastro de Produto ---")
    nome = input("Nome: ")
    categoria = input("Categoria: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade inicial: "))

    produto = {
        "id": proximo_id,
        "nome": nome,
        "categoria": categoria,
        "preco": preco,
        "quantidade": quantidade
    }

    produtos.append(produto)
    proximo_id += 1
    print("Produto cadastrado com sucesso!\n")


def excluir_produto():
    print("\n--- Excluir Produto ---")
    id_buscado = int(input("Digite o ID do produto que deseja excluir: "))

    for produto in produtos:
        if produto["id"] == id_buscado:
            produtos.remove(produto)
            print("Produto removido com sucesso!\n")
            return

    print("Produto não encontrado.\n")


# ----------------------------
#   MOVIMENTAÇÃO DE ESTOQUE
# ----------------------------
def movimentar_estoque():
    print("\n--- Movimentação de Estoque ---")
    id_prod = int(input("ID do produto: "))

    for produto in produtos:
        if produto["id"] == id_prod:
            print(f"Produto encontrado: {produto['nome']} (Qtd atual: {produto['quantidade']})")
            tipo = input("Entrada ou Saída? (E/S): ").upper()

            if tipo not in ("E", "S"):
                print("Operação inválida.\n")
                return

            quantidade = int(input("Quantidade: "))

            if tipo == "E":
                produto["quantidade"] += quantidade
                print("Entrada registrada com sucesso!\n")
            else:
                if quantidade > produto["quantidade"]:
                    print("Erro: estoque insuficiente.\n")
                else:
                    produto["quantidade"] -= quantidade
                    print("Saída registrada com sucesso!\n")
            return

    print("Produto não encontrado.\n")


# ----------------------------
#   RELATÓRIO DE ESTOQUE
# ----------------------------
def mostrar_relatorio():
    print("\n--- Relatório de Produtos ---")
    if not produtos:
        print("Nenhum produto cadastrado.\n")
        return

    for produto in produtos:
        alerta = "⚠️ ESTOQUE BAIXO!" if produto["quantidade"] < 5 else ""
        print(f"""
ID: {produto['id']}
Nome: {produto['nome']}
Categoria: {produto['categoria']}
Preço: R${produto['preco']:.2f}
Quantidade: {produto['quantidade']} {alerta}
        """)

    print("------------------------------\n")


# ----------------------------
#   GRÁFICOS INDIVIDUAIS
# ----------------------------
def grafico_evolucao():
    nomes = [p["nome"] for p in produtos]
    quantidades = [p["quantidade"] for p in produtos]

    plt.figure()
    plt.plot(nomes, quantidades, marker='o')
    plt.title("Evolução do Estoque por Produto")
    plt.xlabel("Produto")
    plt.ylabel("Quantidade")
    plt.grid(True)
    plt.show()


def grafico_categorias():
    categorias = {}
    for p in produtos:
        categorias[p["categoria"]] = categorias.get(p["categoria"], 0) + p["quantidade"]

    plt.figure()
    plt.bar(categorias.keys(), categorias.values())
    plt.title("Comparação de Estoque por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Quantidade Total")
    plt.show()


def grafico_abc():
    valores = sorted(
        [p["preco"] * p["quantidade"] for p in produtos],
        reverse=True
    )

    plt.figure()
    plt.plot(range(1, len(valores) + 1), valores, marker='o')
    plt.title("Curva ABC de Custos de Estoque")
    plt.xlabel("Posição do Item (Ordenado por Custo)")
    plt.ylabel("Custo Total")
    plt.grid(True)
    plt.show()


# ----------------------------
#   MENU DE DASHBOARD
# ----------------------------
def Controle_grafico_de_produtos():
    if not produtos:
        print("Nenhum produto cadastrado para gerar gráficos.\n")
        return

    while True:
        print("""
------ Controle_grafico_de_produtos ------
1 - Evolução do estoque
2 - Barras por categoria
3 - Curva ABC
4 - Voltar ao menu principal
------------------------
        """)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            grafico_evolucao()
        elif opcao == "2":
            grafico_categorias()
        elif opcao == "3":
            grafico_abc()
        elif opcao == "4":
            break
        else:
            print("Opção inválida!\n")


# ----------------------------
#   MENU PRINCIPAL
# ----------------------------
def menu():
    while True:
        print("""
========== MENU ==========
1 - Cadastrar produto
2 - Excluir produto
3 - Movimentar estoque
4 - Mostrar relatório
5 - Controle grafico de produtos
6 - Sair
==========================
        """)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            excluir_produto()
        elif opcao == "3":
            movimentar_estoque()
        elif opcao == "4":
            mostrar_relatorio()
        elif opcao == "5":
            Controle_grafico_de_produtos()
        elif opcao == "6":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida!\n")


menu()