import pandas as pd
import numpy as np

## PUNTO A) ##

# Función para transformar columnas de un dataset a datetime.
def transformar_columnas_datetime(df):
    for columna in df.columns:
        try:
            df[columna] = pd.to_datetime(df[columna])
        except ValueError:
            pass
    return df


# Función para calcular el delta_timing
def calcular_time_delta(df, columna_fecha_inicio, columna_fecha_fin):
    df['time_delta'] = (df[columna_fecha_fin] - df[columna_fecha_inicio]).dt.days
    return df


# Función para calcular el tiempo de entrega.
def tiempo_de_espera(orders, is_delivered=True):
    # filtrar por entregados y crea la varialbe tiempo de espera
    if is_delivered:
        orders = orders.query("order_status=='delivered'").copy()
    # compute wait time
    orders.loc[:, 'tiempo_de_espera'] = \
        (orders['order_delivered_customer_date'] -
         orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')
    return orders


# Función para calcular la diferencia entre la fecha de entrega y la fecha de entrega estimada. si la fecha de entrega real es posterior a la fecha de entrega estimada, devuelve el número de días entre las dos fechas; de lo contrario, devuelve 0
def real_vs_esperado(df, is_delivered=True):
    # Calculo la diferencia entre la fecha de entrega y la fecha de entrega estimada
    df['real_vs_esperado'] = df['order_delivered_carrier_date'] - df['order_estimated_delivery_date']
    # Reemplazo los valores negativos por 0
    df['real_vs_esperado'] = df['real_vs_esperado'].apply(lambda x: x.days)
    df['real_vs_esperado'] = df['real_vs_esperado'].apply(lambda x: 0 if x < 0 else x)
    return df



## PUNTO B) ##

# Función para calcular el puntaje de compra. Entre 1 y 5
def review_score(df):
    df['review_score'] = df['review_score'].apply(lambda x: 1 if x < 3 else 2 if x < 4 else 3 if x < 5 else 4)
    return df



## PUNTO C) ##

# Función para calcular el número de productos por orden.
def calcular_numero_de_productos(orders_items, products):
    # Hago un merge entre los dfs usando la columna 'product_id'
    merged_data = orders_items.merge(products, on='product_id', how='inner')
    # Agrupo por 'order_id' y cuento el número de productos por orden
    product_count_per_order = merged_data.groupby('order_id')['product_id'].count().reset_index()
    product_count_per_order.rename(columns={'product_id': 'number_of_products'}, inplace=True)
    return product_count_per_order



## PUNTO D) ## 

def vendedores_unicos(orders_items):
    # Agrupa por 'order_id' y obtiene el número de vendedores únicos por orden.
    vendedores_unicos_por_orden = orders_items.groupby('order_id')['seller_id'].nunique().reset_index()
    vendedores_unicos_por_orden.rename(columns={'seller_id': 'vendedores_unicos'}, inplace=True)
    return vendedores_unicos_por_orden

# def contar_valores_unicos_por_grupo(data, group_column, value_column):
    # Agrupa por la columna especificada y obtiene el número de valores únicos por grupo
    #resultados = data.groupby(group_column)[value_column].nunique().reset_index()
    #resultados.rename(columns={value_column: f'numero_de_{value_column}'}, inplace=True)

   # return resultados



## PUNTO E) ## 

# Funcion para calcular el precio y el transporte de la order_id
def calcular_precio_y_transporte(order_items, productos):
    # Fusiona los DataFrames usando la columna 'product_id'
    merged_data = order_items.merge(productos, on='product_id', how='inner')
    # Agrupa por 'order_id' y calcula el precio y el transporte de la orden
    precio_y_transporte = merged_data.groupby('order_id').agg({
        'price': 'sum',
        'freight_value': 'sum'
    }).reset_index()
    return precio_y_transporte



## PUNTO F) ## 

from math import radians, sin, cos, asin, sqrt

def calcular_distancia_vendedor_comprador(lon1, lat1, lon2, lat2):
    """
    Computa distancia entre dos pares (lat, lng)
    Ver - (https://en.wikipedia.org/wiki/Haversine_formula)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))