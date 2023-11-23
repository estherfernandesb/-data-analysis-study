import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, inspect, text

url_itens_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/itens_pedidos.csv'
url_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/pedidos.csv'
url_produto = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/produtos.csv'
url_vendedores = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/vendedores.csv'

itens_pedidos = pd.read_csv(url_itens_pedidos)
pedidos = pd.read_csv(url_pedidos)
produtos = pd.read_csv(url_produto)
vendedores = pd.read_csv(url_vendedores)

engine = create_engine('sqlite:///:memory:')

produtos.to_sql('produtos', engine, index = False)

itens_pedidos.to_sql('itens_pedidos', engine, index=False)
pedidos.to_sql('pedidos', engine, index=False)
vendedores.to_sql('vendedores', engine, index=False)

inspetor = inspect(engine)
print(inspetor.get_table_names())

query = 'SELECT CONDICAO FROM PRODUTOS'

def sql_df(query):
    with engine.connect() as conexao:
        consulta = conexao.execute(text(query))
        dados = consulta.fetchall()
    return pd.DataFrame(dados, columns= consulta.keys())

query = '''SELECT CONDICAO, COUNT(*) AS 'Quantidade' FROM PRODUTOS GROUP BY CONDICAO;'''
df_produtos = sql_df(query)

plt.bar(df_produtos['Condicao'], df_produtos['Quantidade'], color = '#3CB371')
plt.title('Contagem por tipos de condições dos produtos')
plt.show()

sql_df('SELECT * FROM PRODUTOS').head(3)
sql_df('SELECT * FROM ITENS_PEDIDOS').head(3)

query = '''SELECT ITENS_PEDIDOS.PRODUTO_ID, PRODUTOS.PRODUTO, SUM(ITENS_PEDIDOS.QUANTIDADE) AS 'Quantidade'
FROM ITENS_PEDIDOS, PRODUTOS WHERE ITENS_PEDIDOS.PRODUTO_ID = PRODUTOS.PRODUTO_ID
GROUP BY PRODUTOS.PRODUTO
ORDER BY Quantidade DESC'''

df_prod_quant = sql_df(query)
plt.barh(df_prod_quant['produto'][-10:], df_prod_quant['Quantidade'][-10:], color = '#3CB371')
plt.xlabel('Quantidade vendida')
plt.show()

sql_df('SELECT * FROM PEDIDOS').head(3)
sql_df('SELECT * FROM PEDIDOS').info()

query = '''SELECT VENDEDORES.NOME_VENDEDOR, AVG(PEDIDOS.TOTAL) AS 'Valor médio de vendas' 
FROM PEDIDOS, VENDEDORES 
WHERE strftime('%Y', data_compra) = '2020' AND VENDEDORES.VENDEDOR_ID = PEDIDOS.VENDEDOR_ID
GROUP BY VENDEDORES.NOME_VENDEDOR
ORDER BY AVG(PEDIDOS.TOTAL) DESC;'''
sql_df(query)

query = '''SELECT ESTADO, COUNT(*) AS Pedidos
FROM ITENS_PEDIDOS
GROUP BY ESTADO
ORDER BY Pedidos DESC;
'''
sql_df(query)

query = '''SELECT VENDEDORES.NOME_VENDEDOR, COUNT(*) AS quantidade_vendas
FROM PEDIDOS
JOIN VENDEDORES ON VENDEDORES.VENDEDOR_ID = PEDIDOS.VENDEDOR_ID
JOIN ITENS_PEDIDOS ON ITENS_PEDIDOS.PEDIDO_ID = PEDIDOS.PEDIDO_ID
WHERE ITENS_PEDIDOS.ESTADO = 'BR-SP'
GROUP BY VENDEDORES.NOME_VENDEDOR
ORDER BY quantidade_vendas DESC;
'''
sql_df(query)
