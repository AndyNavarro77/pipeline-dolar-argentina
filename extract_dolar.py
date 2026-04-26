from sqlalchemy import create_engine
import requests
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# -------------------------
# API CONFIGURATION
# -------------------------
URL = "https://dolarapi.com/v1/dolares"
DATA_PATH = "data/dolar_data.csv"

# -------------------------
# DATABASE CONFIGURATION
# -------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# -------------------------
# EMAIL CONFIGURATION
# -------------------------
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# -------------------------
# FUNCTION: SEND EMAIL REPORT
# -------------------------
def enviar_reporte_mail(df):
    try:
        def get_venta(tipo):
            try:
                return f"${df[df['tipo_dolar'] == tipo]['precio_venta'].iloc[-1]:,.0f}".replace(",", ".")
            except:
                return "N/A"

        def get_spread():
            try:
                oficial = df[df['tipo_dolar'] == 'oficial']['precio_venta'].iloc[-1]
                blue = df[df['tipo_dolar'] == 'blue']['precio_venta'].iloc[-1]
                spread = ((blue - oficial) / oficial) * 100
                return f"{spread:.1f}%".replace(".", ",")
            except:
                return "N/A"

        fecha_hora = datetime.now().strftime("%m/%d/%Y · %I:%M %p")
        oficial = get_venta('oficial')
        blue = get_venta('blue')
        bolsa = get_venta('bolsa')
        mayorista = get_venta('mayorista')
        ccl = get_venta('ccl')
        cripto = get_venta('cripto')
        tarjeta = get_venta('tarjeta')
        spread = get_spread()
        total = len(df)

        html = f"""
        <html><body style="margin:0;padding:0;font-family:Arial,sans-serif;background:#f4f4f4;">
        <div style="max-width:600px;margin:20px auto;background:#ffffff;border-radius:10px;overflow:hidden;border:1px solid #e0e0e0;">

          <div style="background:#0C447C;padding:24px 28px;">
            <h1 style="color:#E6F1FB;font-size:18px;font-weight:600;margin:0 0 4px;">Pipeline Successful — Argentina FX Monitor</h1>
            <p style="color:#85B7EB;font-size:13px;margin:0;">Automated daily report · {fecha_hora}</p>
          </div>

          <div style="padding:24px 28px;">
            <p style="font-size:14px;color:#555;margin:0 0 16px;">Hi Andrés, the pipeline ran successfully. Here is today's exchange rate summary:</p>

            <table width="100%" cellspacing="0" cellpadding="0" style="margin-bottom:20px;">
              <tr>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:12px 14px;">
                    <p style="font-size:11px;color:#888;margin:0 0 4px;">Official Rate</p>
                    <p style="font-size:20px;font-weight:600;color:#3B6D11;margin:0;">{oficial}</p>
                  </div>
                </td>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:12px 14px;">
                    <p style="font-size:11px;color:#888;margin:0 0 4px;">Blue Rate</p>
                    <p style="font-size:20px;font-weight:600;color:#185FA5;margin:0;">{blue}</p>
                  </div>
                </td>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:12px 14px;">
                    <p style="font-size:11px;color:#888;margin:0 0 4px;">Bolsa Rate</p>
                    <p style="font-size:20px;font-weight:600;color:#333;margin:0;">{bolsa}</p>
                  </div>
                </td>
                <td width="25%" style="padding:4px;">
                  <div style="background:#f5f5f5;border-radius:8px;padding:12px 14px;">
                    <p style="font-size:11px;color:#888;margin:0 0 4px;">Informal Spread</p>
                    <p style="font-size:20px;font-weight:600;color:#BA7517;margin:0;">{spread}</p>
                  </div>
                </td>
              </tr>
            </table>

            <table width="100%" style="font-size:13px;border-collapse:collapse;margin-bottom:16px;">
              <tr style="border-top:1px solid #eee;"><td style="padding:7px 4px;color:#888;">Wholesale (Mayorista)</td><td style="padding:7px 4px;text-align:right;font-weight:600;">{mayorista}</td></tr>
              <tr style="border-top:1px solid #eee;"><td style="padding:7px 4px;color:#888;">CCL</td><td style="padding:7px 4px;text-align:right;font-weight:600;">{ccl}</td></tr>
              <tr style="border-top:1px solid #eee;"><td style="padding:7px 4px;color:#888;">Crypto</td><td style="padding:7px 4px;text-align:right;font-weight:600;">{cripto}</td></tr>
              <tr style="border-top:1px solid #eee;"><td style="padding:7px 4px;color:#888;">Card Rate (Tarjeta)</td><td style="padding:7px 4px;text-align:right;font-weight:600;">{tarjeta}</td></tr>
              <tr style="border-top:1px solid #eee;"><td style="padding:7px 4px;color:#888;">Total records processed</td><td style="padding:7px 4px;text-align:right;font-weight:600;">{total}</td></tr>
            </table>

            <div style="background:#FAEEDA;border:1px solid #EF9F27;border-radius:8px;padding:12px 14px;font-size:13px;color:#633806;">
              &#9888; Active alert: automated email notification if Blue Rate exceeds <strong>$1,600 ARS</strong> — configured via n8n.
            </div>
          </div>

          <div style="padding:12px 28px;background:#f9f9f9;border-top:1px solid #eee;font-size:12px;color:#aaa;">
            <span>Automated pipeline · Task Scheduler + n8n</span>&nbsp;&nbsp;|&nbsp;&nbsp;
            <span>Andrés Navarro · github.com/AndyNavarro77</span>
          </div>

        </div>
        </body></html>
        """

        msg = EmailMessage()
        msg['Subject'] = f"✅ Pipeline Successful — Official: {oficial} | Blue: {blue} | Spread: {spread}"
        msg['From'] = EMAIL_REMITENTE
        msg['To'] = EMAIL_REMITENTE
        msg.set_content("This email requires an HTML-compatible email client.")
        msg.add_alternative(html, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# -------------------------
# FUNCTION: EXTRACT DATA
# -------------------------
def extraer_datos():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching data:", e)
        return None

# -------------------------
# FUNCTION: TRANSFORM DATA
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
# FUNCTION: SIMULATE HISTORICAL DATA
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
# FUNCTION: SAVE TO CSV
# -------------------------
def guardar_csv(df):
    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv(DATA_PATH, index=False)
    print("Data saved to CSV")

# -------------------------
# FUNCTION: CONNECT TO MYSQL
# -------------------------
def conectar_db():
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        return engine
    except Exception as e:
        print("Error connecting to MySQL:", e)
        return None

# -------------------------
# FUNCTION: INSERT DATA (UPSERT)
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
        print("Data loaded into MySQL successfully")
        return True
    except Exception as e:
        print("Error inserting data:", e)
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

        print("Pipeline completed successfully.")
    else:
        print("Pipeline could not be executed.")