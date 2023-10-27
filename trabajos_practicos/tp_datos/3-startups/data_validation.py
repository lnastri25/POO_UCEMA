import pandas as pd

def validate_columns(df):
    # Resumen de las estadísticas de las columnas.
    summary_df = df.describe(include='all').T

    # Agrego el numero de valores nulos al resumen del DataFrame.
    summary_df['Num_Null_Values'] = df.isnull().sum()

    # Agrego el porcentaje de valores nulos al resumen del DataFrame.
    summary_df['%_Null_Values'] = (summary_df['Num_Null_Values'] / len(df)) * 100

    # Agarro los valores únicos de una muestra de 5 filas.
    sample_unique_values = df.sample(min(5, len(df)), axis=0).T

    # Agrego los valores únicos de la muestra al resumen del DataFrame.
    summary_df['Sample_Unique_Values'] = sample_unique_values.values.tolist()

    # Renombrar las columnas del resumen del DataFrame.
    summary_df = summary_df.rename(columns={'unique': 'Unique_Values', 'count': 'Num_Unique_Values'})

    # Reordeno las columnas del resumen del DataFrame.
    summary_df = summary_df[['Unique_Values', 'Num_Unique_Values', 'Num_Null_Values', '%_Null_Values', 'Sample_Unique_Values']]

    return summary_df
