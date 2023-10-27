import pandas as pd

## FUNCIÓN PARA CARGAR EL DATAFRAME ##

def load_df(path):
    df = pd.read_csv(path)
    return df

# from funcionesPOO import load_df
# df = load_df('data.csv')




## FUNCIÓN PARA VALIDAR COLUMNAS ##

def validate_columns(df):
    summary_df = df.describe(include='all').T
    summary_df['Num_Null_Values'] = df.isnull().sum().
    summary_df['%_Null_Values'] = (summary_df['Num_Null_Values'] / len(df)) * 100
    sample_unique_values = df.sample(min(5, len(df)), axis=0).T
    summary_df['Sample_Unique_Values'] = sample_unique_values.values.tolist()
    summary_df = summary_df.rename(columns={'unique': 'Unique_Values', 'count': 'Num_Unique_Values'})
    summary_df = summary_df[['Unique_Values', 'Num_Unique_Values', 'Num_Null_Values', '%_Null_Values', 'Sample_Unique_Values']]

    return summary_df

# from funcionesPOO import validate_columns
# validate_columns(df)