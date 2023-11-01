import pandas as pd
import matplotlib.pyplot as plt

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