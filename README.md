Este projeto é um sistema de gestão de estoque inspirado em módulos reais de ERPs (Enterprise Resource Planning). O objetivo é permitir o controle básico de produtos, movimentações, relatórios e visualizações gráficas, tudo funcionando em linha de comando, com persistência usando SQLite.

Tecnologias utilizadas

Python 3

SQLite3 — banco de dados local embutido no Python

Matplotlib — criação dos gráficos do dashboard

Datetime — manipulação de datas e cálculo de reabastecimento

Funcionalidades principais
Cadastro de produtos

Nome

Categoria

Preço

Quantidade inicial

Registro automático da data da última movimentação

Exclusão de produtos

Remove um item do banco via ID.

Confirmação antes da exclusão.

Movimentação de estoque

Entrada e saída de produtos.

Impede saída maior que o estoque disponível.

Atualiza automaticamente a data da última movimentação.

Relatório completo

Exibe para cada produto:

ID

Nome

Categoria

Preço

Quantidade

Última movimentação

Alerta para estoque baixo (menos de 5 unidades)

Previsão de Reabastecimento

Calcula, com base no consumo médio diário informado, quanto tempo o estoque atual ainda dura e a data estimada de término.

Dashboard gráfico

Organizado em um menu separado com três gráficos:

Evolução do estoque por produto

Comparação de categorias (gráfico de barras)

Curva ABC de custos de estoque

Os gráficos fornecem visão gerencial semelhante a sistemas ERP reais.

Organização do Banco de Dados (SQLite)

A tabela produtos contém:

Coluna	Tipo	Descrição
id	INTEGER	Identificador único
nome	TEXT	Nome do produto
categoria	TEXT	Categoria geral
preco	REAL	Preço unitário
quantidade	INTEGER	Quantidade atual
ultima_movimentacao	TEXT	Data/hora da última alteração

A criação e atualização da tabela são automáticas ao rodar o programa.

Como executar

Instale as dependências:

pip install matplotlib

(SQLite já vem com o Python)

Execute:

python seu_arquivo.py

O sistema cria automaticamente o banco estoque.db e abre o menu principal.

Objetivo do projeto

O código foi desenvolvido para fins educacionais, simulando as principais funcionalidades de um módulo de estoque de sistemas ERP.
Ele demonstra:

Persistência de dados

Manipulação de banco SQLite

Criação de dashboards

Cálculo de previsões

Lógica de negócios de estoque
