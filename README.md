Este código implementa um sistema de gestão de estoque em Python, com funcionalidades inspiradas em módulos comuns de ERPs (Enterprise Resource Planning),
e estrutura voltada para o controle, análise, manutenção e visualização de informações de produtos em estoque. O sistema é pensado para facilitar o cadastro,
atualização, exclusão, monitoramento, geração de relatórios e gráficos gerenciais, utilizando boas práticas e conceitos próximos ao que grandes sistemas ERP adotam.

Bibliotecas usadas
- sqlite3: utilizada para manipulação de bancos de dados SQLite, garantindo fácil armazenamento e consulta dos dados dos produtos e histórico de movimentações.
- datetime: para tratamento e cálculo de datas, como tempo de reposição de produtos.
- collections.defaultdict: auxilia na organização de dados e agrupamento por produto, especialmente útil para relatórios e gráficos históricos.
- matplotlib.pyplot: para geração de gráficos gerenciais, como evolução do estoque, comparação entre categorias e curva ABC de custos.

Por que dois bancos de dados?
- O sistema utiliza duas tabelas principais (que podem estar em um ou dois arquivos dependendo da implementação física): uma para os produtos do estoque ("reservatorio.db")
  e outra para o histórico de movimentações ("historicoestoque").
- O uso de duas estruturas permite separar a tabela base dos produtos (dados estáticos: nome, categoria, preço, quantidade, estoque mínimo) do registro histórico de entradas
  e saídas (dados dinâmicos: movimentação ao longo do tempo), facilitando consultas gerenciais sem misturar informações ou comprometer desempenho.

Funcionalidades presentes
- Cadastro, exclusão e validação de produtos, incluindo controles de categoria, preço unitário, quantidade inicial e estoque mínimo.
- Atualização dinâmica do estoque, permitindo entradas e saídas, com checagem do estoque mínimo para alertas automáticos.
- Listagem do estoque com status de cada produto e detecção de itens em nível baixo de estoque.
- Relatórios gerenciais com cálculos automáticos (giro de estoque, custo de manutenção de estoque, tempo de reposição e vendas no período).
- Gráficos avançados: mostra evolução do estoque por produto, compara categorias e exibe curva ABC, fundamentando decisões de compra, reposição e análise financeira do estoque.
- Cada uma dessas funções reflete práticas reais utilizadas em sistemas ERP, facilitando integração futura ou migração para plataformas maiores, além de permitir controle e
  tomada de decisão baseada em dados.
