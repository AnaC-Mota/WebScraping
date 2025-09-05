import pandas as pd
import sqlite3
from datetime import datetime

df = pd.read_json('data/data.jsonl', lines = True)

pd.options.display.max_columns = None

df['_source'] = "https://lista.mercadolivre.com.br/notebook"
df['_datetime'] = datetime.now()


# Tratar nulos
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating'] = df['reviews_rating'].fillna('0')
df['reviews_total'] = df['reviews_total'].fillna('(0)')

# Garantir que estão como strings antes de usar .str
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex=False)
df['reviews_total'] = df['reviews_total'].astype(str).str.replace(r'[\(\)]', '', regex=True)

# Converter para números
df['old_money'] = df['old_money'].astype(float)
df['new_money'] = df['new_money'].astype(float)
df['reviews_rating'] = df['reviews_rating'].astype(float)
df['reviews_total'] = df['reviews_total'].astype(int)

# Tratar os preços como floats e calcular os valores totais
# Manter apenas produtos com preço entre 1000 e 10000 reais
df = df[
    (df['old_money'] >= 1000) & (df['old_money'] <= 10000) &
    (df['new_money'] >= 1000) & (df['new_money'] <= 10000)
]

conn = sqlite3.connect('data/mercadolivre.db')

df.to_sql('notebook', conn, if_exists='replace', index=False)

conn.close()

print(df)