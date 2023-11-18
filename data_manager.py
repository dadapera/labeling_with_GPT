import pandas as pd

file_path = 'data/training_test.csv'
df = pd.read_csv(file_path, sep=";")

df = df.drop(columns=["url","brand","valuePackage","basePrice","price","img","code"])

df['query_text'] = df.apply(lambda row: '/'.join(map(str, row)), axis=1)

random_rows = df.sample(n=10)

for i,r in zip(random_rows.index,random_rows["query_text"]):
    print(i,r)


'''print(
    {
        "id": df.index[0],
        "product": df.loc[0]['query_text']
    }
    )
'''