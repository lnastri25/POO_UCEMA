import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


## FUNCIÓN PARA CARGAR EL DATAFRAME ##

def load_df(path):
    df = pd.read_csv(path)
    return df


## GENERALES ##

def whitespace_remover_and_columns(dataframe):
    # itero sobre las columnas
    for i in dataframe.columns:
        # chequeo si la columna es de tipo object
        if dataframe[i].dtype == 'object':
            # aplico la función strip a la columna
            dataframe[i] = dataframe[i].map(str.strip)
        else:
            # si la condición es Falsa, no hará nada.
            pass
    dataframe.rename(columns=lambda x: x.strip(), inplace=True)
    return dataframe


## FUNCIÓN PARA VALIDAR COLUMNAS ##

def validate_columns(df):
    summary_df = df.describe(include='all').T
    summary_df['Num_Null_Values'] = df.isnull().sum()
    summary_df['%_Null_Values'] = (summary_df['Num_Null_Values'] / len(df)) * 100
    sample_unique_values = df.sample(min(5, len(df)), axis=0).T
    summary_df['Sample_Unique_Values'] = sample_unique_values.values.tolist()
    summary_df = summary_df.rename(columns={'unique': 'Unique_Values', 'count': 'Num_Unique_Values'})
    summary_df = summary_df[['Unique_Values', 'Num_Unique_Values', 'Num_Null_Values', '%_Null_Values', 'Sample_Unique_Values']]

    return summary_df


## FUNCIÓN PARA GRAFICAR VALORES OUTLIERS ##

def plot_outliers(df):
    num_cols = df.select_dtypes(include=['float64', 'int64']).shape[1]
    num_rows = (num_cols - 1) // 2 + 1
    fig, axs = plt.subplots(num_rows, 2, figsize=(20, 5*num_rows))
    axs = axs.flatten()
    for i, col in enumerate(df.select_dtypes(include=['float64', 'int64']).columns):
        box = axs[i].boxplot(df[col], patch_artist=True, boxprops=dict(facecolor='#336fa2'), medianprops=dict(color='black'))
        for patch in box['fliers']:
            patch.set_markerfacecolor('black')
            patch.set_markeredgecolor('black')
        axs[i].set_title(col)
    plt.tight_layout()
    plt.show()


## FUNCIÓN PARA DETERMINAR SI ¿ES OUTLIER O NO? ##

def is_outlier(data, scale_factor=1.5):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - scale_factor * iqr
    upper_bound = q3 + scale_factor * iqr
    return (data < lower_bound) | (data > upper_bound)


"""
from funciones.exploratory_data_analysis import is_outlier

outliers_admin_costs = is_outlier(df_startups["Admin_Costs"], 1.5)
outlier_values_admin_costs = df_startups["Admin_Costs"][outliers_admin_costs]

outliers_net_profit = is_outlier(df_startups["Net_Profit"], 1.5)
outlier_values_net_profit = df_startups["Net_Profit"][outliers_net_profit]

outliers_profit = is_outlier(df_startups["Profit"], 1.5)
outlier_values_profit = df_startups["Profit"][outliers_net_profit]


print("Outliers de Admin_Costs:")
print(outlier_values_admin_costs)
print("")
print("Outliers de Net_Profit:")
print(outlier_values_net_profit)
print("")
print("Outliers de Profit:")
print(outlier_values_profit)
"""



## FUNCIÓN PARA CREAR HEATMAP DE CORRELACIÓN ENTRE VARIABLES NUMÉRICAS ##

def crear_heatmap_correlacion(df): # --> pasarle siempre el df original, nada de filtrado.
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


## FUNCIÓN PARA TRANSFORMAR COLUMNAS A DATETIME ##

def transformar_columnas_datetime(df):
    for columna in df.columns:
        try:
            df[columna] = pd.to_datetime(df[columna])
        except ValueError:
            pass
    return df
