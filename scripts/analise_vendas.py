
import os
os.makedirs("../data", exist_ok=True)
import pandas as pd
import random
from faker import Faker

# Inicializa o gerador de dados
fake = Faker('pt_BR')
random.seed(42)

# Configurações
num_registros = 500
categorias_produtos = {
    "Eletrônicos": ["Fone de Ouvido", "Smartphone", "Notebook", "Carregador", "Mouse"],
    "Casa": ["Liquidificador", "Aspirador", "Panela Elétrica", "Cafeteira"],
    "Moda": ["Camisa", "Calça Jeans", "Tênis", "Jaqueta"],
    "Beleza": ["Perfume", "Shampoo", "Hidratante", "Maquiagem"]
}
regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

# Geração dos dados de vendas
dados = []

for _ in range(num_registros):
    categoria = random.choice(list(categorias_produtos.keys()))
    produto = random.choice(categorias_produtos[categoria])
    quantidade = random.randint(1, 10)
    preco_unitario = round(random.uniform(20, 1500), 2)
    data_venda = fake.date_between(start_date='-6M', end_date='today')
    regiao = random.choice(regioes)
    vendedor = fake.first_name()

    dados.append([
        data_venda, produto, categoria, quantidade,
        preco_unitario, quantidade * preco_unitario,
        regiao, vendedor
    ])

# DataFrame base
colunas = ["Data da Venda", "Produto", "Categoria", "Quantidade", "Preço Unitário", "Receita", "Região", "Vendedor"]
df = pd.DataFrame(dados, columns=colunas)

# Tratamento
df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
df["Ano"] = df["Data da Venda"].dt.year
df["Mês"] = df["Data da Venda"].dt.strftime('%B')

# Resumos
resumo_categoria = df.groupby("Categoria")["Receita"].sum().reset_index()
resumo_produto = df.groupby("Produto")["Receita"].sum().reset_index()
resumo_regiao = df.groupby("Região")["Receita"].sum().reset_index()
resumo_mes = df.groupby("Mês")["Receita"].sum().reset_index()
resumo_vendedor = df.groupby("Vendedor")["Receita"].sum().reset_index()

# Salvando arquivos
df.to_excel("../data/vendas_simuladas.xlsx", index=False)

with pd.ExcelWriter("../data/analise_vendas.xlsx") as writer:
    df.to_excel(writer, sheet_name="Base de Vendas", index=False)
    resumo_categoria.to_excel(writer, sheet_name="Por Categoria", index=False)
    resumo_produto.to_excel(writer, sheet_name="Por Produto", index=False)
    resumo_regiao.to_excel(writer, sheet_name="Por Região", index=False)
    resumo_mes.to_excel(writer, sheet_name="Por Mês", index=False)
    resumo_vendedor.to_excel(writer, sheet_name="Por Vendedor", index=False)

print("Arquivos gerados com sucesso na pasta /data!")