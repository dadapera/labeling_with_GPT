import pandas as pd

def load_data(file_path, chunk_size):
    csv_reader = pd.read_csv(file_path, sep=";", chunksize=chunk_size)
    return csv_reader
    

def save_df_as_csv(df, file_path):
    df.to_csv(file_path, sep=';')


def append_df_to_csv(df_new, csv_existing):
    df_existing = pd.read_csv(csv_existing, sep=';')
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(csv_existing, index=False, sep=';')

