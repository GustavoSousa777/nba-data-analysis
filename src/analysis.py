import pandas as pd
import numpy as np
import mysql.connector

df = pd.read_csv("../data/nba_data_processed.csv")

# print(df.info())

print("Linhas e colunas antes:",df.shape)

df = df.dropna(how='all')


print("Linhas e colunas depois:",df.shape)

cols_percent = ['FG%', '3P%', '2P%', 'eFG%', 'FT%']

df[cols_percent] = df[cols_percent].fillna(0)

print("\nValores nulos após tratamento:")
print(df.isnull().sum())

# Metricas:

# Pontos por minuto
df['PTS_per_min'] = np.where(df['MP'] > 0 , df['PTS'] / df['MP'], 0)

# Assistências por jogo
df['AST_per_game'] = np.where(df['G'] > 0, df['AST'] / df['G'], 0)

# Rebotes por jogo
df['TRB_per_game']= np.where(df['G'] > 0 , df['TRB']/df['G'], 0)

# Score geral (métrica que eu criei)
df['Score'] = (
    df['PTS'] * 0.5 +
    df['AST'] * 0.2 +
    df['TRB'] * 0.2 -
    df['TOV'] * 0.1
)

# Segmentação de jogadores
df['Player_Type'] = np.where(
    (df['PTS'] > df['PTS'].mean()) &
    (df['PTS_per_min'] > df['PTS_per_min'].mean()),
    'Elite',
    'Regular'
)

# Algumas Análises: 
print("\nTop 10 pontuadores:")
print(df.sort_values(by='PTS', ascending=False)[['Player', 'PTS']].head(10))

print("\nTop 10 eficientes:")
print(df[df['MP'] >= 10]
      .sort_values(by='PTS_per_min', ascending=False)
      [['Player', 'PTS_per_min']]
      .head(10))

print("\nTop Score geral:")
print(df.sort_values(by='Score', ascending=False)[['Player', 'Score']].head(10))

print("\nMédia de pontos por posição:")
print(df.groupby('Pos')['PTS'].mean().sort_values(ascending=False))

print("\nMédia de pontos por time:")
print(df.groupby('Tm')['PTS'].mean().sort_values(ascending=False))

#  Conectando e enviando para o MYSQL
df.columns = df.columns.str.replace('%' , 'pct')
df = df.replace({np.nan: None})
conn = mysql.connector.connect(
    host = '127.0.0.1',
    port = 3308,
    user = '****',
    password ='********',
    database = 'nba_analysis'
)
cursor = conn.cursor()

print("\nConectado ao MySQL!")

# Limpando tabela dos teste que fiz para evitar duplicação
cursor.execute("DELETE FROM nba_players")
conn.commit()

print("Tabela limpa!")

# Inserindo os dados
columns = ",".join(df.columns)
placeholders = ",".join(["%s"] * len(df.columns))

sql = f"INSERT INTO nba_players ({columns}) VALUES ({placeholders})"

data = [tuple(row) for _, row in df.iterrows()]

cursor.executemany(sql, data)
conn.commit()

print("Dados enviados para o MySQL com sucesso!")

# Validando Conexão

cursor.execute("SELECT COUNT(*) FROM nba_players")
total = cursor.fetchone()[0]

print(f"Total de linhas no banco: {total}")
# Encerrando conexão
cursor.close()
conn.close()

print("Conexão encerrada.")

