from sqlalchemy import create_engine
import requests
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

# -------------------------
# CONFIGURACIÓN API
# -------------------------
URL = "https://dolarapi.com/v1/dolares"
DATA_PATH = "data/dolar_data.csv"

# -------------------------
# CONFIGURACIÓN BASE DE DATOS
# -------------------------
DB_USER = "root"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "pipeline_dolar"

# -------------------------
# CONFIGURACIÓN EMAIL 
# -------------------------
EMAIL_REMITENTE = "andresnavarroalvarez15@gmail.com"
EMAIL_PASSWORD = "ikajsdosbxftunoe" # Pegado sin espacios

# -------------------------
# FUNCIÓN: ENVIAR REPORTE POR MAIL
# -------------------------
def enviar_reporte_mail(df):
    try:
        valor_blue = df[df['tipo_dolar'] == 'blue']['precio_venta'].iloc[-1]
        
        msg = EmailMessage()
        msg['Subject'] = f"✅ Pipeline Exitoso - Dólar Blue: ${valor_blue}"
        msg['From'] = EMAIL_REMITENTE
        msg['To'] = EMAIL_REMITENTE 
        
        contenido = f"""Hola Andres,
        
El pipeline de datos se ejecutó correctamente.
- Datos actualizados en MySQL y CSV.
- Referencia Dólar Blue: ${valor_blue}
- Total de registros procesados (histórico): {len(df)}

Saludos,"""

        msg.set_content(contenido)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Notificación de email enviada con éxito.")
    except Exception as e:
        print(f"Error al enviar el email: {e}")

# -------------------------
# FUNCIÓN: EXTRAER DATOS
# -------------------------
def extraer_datos():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("Error al obtener datos:", e)
        return None

# -------------------------
# FUNCIÓN: TRANSFORMAR
# -------------------------
def transformar_datos(data):
    df = pd.DataFrame(data)
    df['fechaActualizacion'] = pd.to_datetime(df['fechaActualizacion'])
    df = df.rename(columns={
        'casa': 'tipo_dolar',
        'compra': 'precio_compra',
        'venta': 'precio_venta',
        'fechaActualizacion': 'fecha'
    })
    df = df[['tipo_dolar', 'nombre', 'precio_compra', 'precio_venta', 'fecha']]
    return df

# -------------------------
# FUNCIÓN: SIMULAR HISTÓRICO
# -------------------------
def simular_historico(df):
    historico = []
    for i in range(30):
        df_temp = df.copy()
        df_temp['fecha'] = df_temp['fecha'] - pd.Timedelta(days=i)
        variacion = 1 + (i * 0.003)
        df_temp['precio_compra'] = df_temp['precio_compra'] * variacion
        df_temp['precio_venta'] = df_temp['precio_venta'] * variacion
        historico.append(df_temp)
    
    df_final = pd.concat(historico)
    df_final = df_final.sort_values(by='fecha')
    return df_final

# -------------------------
# FUNCIÓN: GUARDAR CSV
# -------------------------
def guardar_csv(df):
    # Asegura que la carpeta data exista donde sea que se ejecute el script
    if not os.path.exists("data"):
        os.makedirs("data")
    
    df.to_csv(DATA_PATH, index=False)
    print("Datos guardados en CSV")

# -------------------------
# FUNCIÓN: CONECTAR A MYSQL
# -------------------------
def conectar_db():
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        return engine
    except Exception as e:
        print("Error al conectar a MySQL:", e)
        return None

# -------------------------
# FUNCIÓN: INSERTAR DATOS (UPSERT)
# -------------------------
def cargar_a_mysql(df, engine):
    try:
        with engine.begin() as connection:
            for _, row in df.iterrows():
                query = """
                INSERT INTO dolar (tipo_dolar, nombre, precio_compra, precio_venta, fecha)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    precio_compra = VALUES(precio_compra),
                    precio_venta = VALUES(precio_venta)
                """
                connection.exec_driver_sql(query, (
                    row['tipo_dolar'],
                    row['nombre'],
                    row['precio_compra'],
                    row['precio_venta'],
                    row['fecha']
                ))
        print("Datos cargados en MySQL correctamente")
        return True
    except Exception as e:
        print("Error al insertar datos:", e)
        return False

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    data = extraer_datos()

    if data:
        df = transformar_datos(data)
        df = simular_historico(df)
        guardar_csv(df)
        engine = conectar_db()

        if engine:
            exito = cargar_a_mysql(df, engine)
            if exito:
                enviar_reporte_mail(df)
        
        print("Pipeline finalizado con éxito.")
    else:
        print("No se pudo ejecutar el pipeline")
