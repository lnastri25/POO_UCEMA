import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


## FUNCIÓN PARA CREAR HEATMAP DE CORRELACIÓN ENTRE VARIABLES NUMÉRICAS ##

def crear_heatmap_correlacion(df):
    def seleccionar_columnas_numericas(df):
        return df.select_dtypes(include=['float64', 'int64'])

    # Seleccionar las columnas numéricas del DataFrame
    df_numeric = seleccionar_columnas_numericas(df)

    # Eliminar las columnas con títulos no deseados
    df_numeric = df_numeric.drop(columns=[col for col in df_numeric.columns if col.startswith("Unnamed:") or col.strip() == ""])

    # Calcular la matriz de correlación
    corr_matrix = df_numeric.corr()

    # Crear el heatmap de correlación
    plt.figure(figsize=(10, 10))
    sns.heatmap(
        round(corr_matrix, 2),
        cmap='coolwarm',
        annot=True,
        annot_kws={"size": 10}
    )
    plt.show()