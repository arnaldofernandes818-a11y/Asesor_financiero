import requests
import schedule
import time
import os
import pytz
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

# ==========================================
# CONFIGURACIÓN PROFESIONAL
# ==========================================
TOKEN = "8138438253:AAGgdSgL67Kt1a0gEcm5NqYedsHKsa9UjN0"
CHAT_ID = "7100105540"
ZONA_HORARIA = pytz.timezone('US/Eastern')

app = Flask(__name__)

@app.route('/')
def home():
    return "🏛️ LACER PRO: CENTRAL INTELLIGENCE OPERATIONAL"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        pass

# ==========================================
# GESTIÓN DE DATOS BINANCE -> TELEGRAM
# ==========================================

def obtener_precios_seguros():
    # Reintento triple para evitar el error de enlace
    for i in range(3):
        try:
            r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT", timeout=10).json()
            r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=10).json()
            return float(r_eur['price']), float(r_oro['price'])
        except:
            time.sleep(2)
    return None, None

def ejecutar_analisis_latigazo(precio_base_eur, precio_base_oro, hora_evento):
    # Espera institucional de 120 segundos
    time.sleep(120) 
    p_final_eur, p_final_oro = obtener_precios_seguros()
    
    if p_final_eur and precio_base_eur:
        var_eur = ((p_final_eur - precio_base_eur) / precio_base_eur) * 100
        var_oro = ((p_final_oro - precio_base_oro) / precio_base_oro) * 100
        
        v_eur = "🔹 EXPANSIÓN ALCISTA" if var_eur > 0.02 else "🔸 DISTRIBUCIÓN BAJISTA" if var_eur < -0.02 else "⚖️ ACUMULACIÓN"
        v_oro = "🔹 EXPANSIÓN ALCISTA" if var_oro > 0.05 else "🔸 DISTRIBUCIÓN BAJISTA" if var_oro < -0.05 else "⚖️ ACUMULACIÓN"

        mensaje = (
            f"🏛️ **INFORME DE IMPACTO INSTITUCIONAL**\n"
            f"⏱️ Referencia: {hora_evento} EST\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🇪🇺 **EURUSD:** {v_eur} ({var_eur:+.4f}%)\n"
            f"🏆 **XAUUSD:** {v_oro} ({var_oro:+.4f}%)\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💼 *Lacer Pro: Análisis de Liquidez Completado.*"
        )
        enviar_telegram(mensaje)

def protocolo_posicionamiento(hora):
    p_eur, p_oro = obtener_precios_seguros()
    if p_eur and p_oro:
        Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()
    else:
        enviar_telegram(f"❌ **ERROR DE CONEXIÓN:** Binance no respondió a las {hora}.")

# ==========================================
# CRONOGRAMA SINCRONIZADO
# ==========================================

def iniciar_cronograma():
    # HORARIOS PARA LAS PRUEBAS DE HOY
    noticias = ["07:00", "07:30", "08:00"]
    
    hora_actual = datetime.now(ZONA_HORARIA).strftime("%H:%M:%S")
    enviar_telegram(f"🏛️ **SISTEMA SINCRONIZADO**\n🕒 Hora Nueva York: {hora_actual}\n✅ Vigilando: 07:00, 07:30, 08:00")

    for hora in noticias:
        # Alerta 10 min antes
        t_pre = (datetime.strptime(hora, "%H:%M") - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_pre).do(enviar_telegram, f"📢 **ALERTA:** Noticia en 10 min ({hora} EST).")
        
        # Punto Cero 2 min antes
        t_pos = (datetime.strptime(hora, "%H:%M") - timedelta(minutes=2)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(protocolo_posicionamiento, hora)

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    iniciar_cronograma()
    while True:
        schedule.run_pending()
        time.sleep(15)
        
