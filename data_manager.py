import pandas as pd

file_path = 'data/training_test.csv'
df = pd.read_csv(file_path, sep=";")

df = df.drop(columns=["url","brand","valuePackage","basePrice","price","img","code"])

df['query_text'] = df.apply(lambda row: '/'.join(map(str, row)), axis=1)

print(df.shape[0])
'''print(
    {
        "id": df.index[0],
        "product": df.loc[0]['query_text']
    }
    )
'''