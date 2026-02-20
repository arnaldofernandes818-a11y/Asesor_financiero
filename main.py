import requests
import schedule
import time
import os
import pytz
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

# ==========================================
# CONFIGURACIÓN DE CONECTIVIDAD PROFESIONAL
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
# NÚCLEO DE INTELIGENCIA DE DATOS
# ==========================================

def obtener_precios():
    try:
        # Petición directa a Binance con timeout de seguridad
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT", timeout=5).json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5).json()
        return float(r_eur['price']), float(r_oro['price'])
    except:
        return None, None

def ejecutar_analisis_latigazo(precio_base_eur, precio_base_oro, hora_evento):
    # ADN de la Estrategia: 120 segundos de espera tras el evento
    time.sleep(120) 
    precio_final_eur, precio_final_oro = obtener_precios()
    
    if precio_final_eur and precio_base_eur:
        var_eur = ((precio_final_eur - precio_base_eur) / precio_base_eur) * 100
        var_oro = ((precio_final_oro - precio_base_oro) / precio_base_oro) * 100
        
        # Veredictos Institucionales
        v_eur = "🔹 EXPANSIÓN ALCISTA" if var_eur > 0.02 else "🔸 DISTRIBUCIÓN BAJISTA" if var_eur < -0.02 else "⚖️ ACUMULACIÓN"
        v_oro = "🔹 EXPANSIÓN ALCISTA" if var_oro > 0.05 else "🔸 DISTRIBUCIÓN BAJISTA" if var_oro < -0.05 else "⚖️ ACUMULACIÓN"

        mensaje = (
            f"🏛️ **INFORME DE IMPACTO INSTITUCIONAL**\n"
            f"⏱️ Referencia: {hora_evento} EST\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🇪🇺 **ACTIVO: EURUSD**\n"
            f"📈 Flujo: {v_eur}\n"
            f"📊 Variación: {var_eur:+.4f}%\n\n"
            f"🏆 **ACTIVO: XAUUSD (ORO)**\n"
            f"📈 Flujo: {v_oro}\n"
            f"📊 Variación: {var_oro:+.4f}%\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 *Lacer Pro: Análisis Fundamental Completado.*"
        )
        enviar_telegram(mensaje)
    else:
        enviar_telegram("⚠️ **FALLO CRÍTICO:** Pérdida de conexión con Binance durante el latigazo.")

def protocolo_posicionamiento(hora):
    p_eur, p_oro = obtener_precios()
    if p_eur and p_oro:
        # Hilo separado para no bloquear el cronograma principal
        Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()
    else:
        enviar_telegram(f"⚠️ **SISTEMA:** Error de enlace para el evento de las {hora}. Reintentando...")

# ==========================================
# CRONOGRAMA OPERATIVO (EST)
# ==========================================

def iniciar_cronograma():
    # HORARIOS SOLICITADOS (Formato 24h)
    noticias = ["12:18", "12:30", "13:01"]
    
    # Mensaje de arranque con hora actual confirmada
    hora_actual = datetime.now(ZONA_HORARIA).strftime("%H:%M:%S")
    enviar_telegram(f"🏛️ **SISTEMA ONLINE (MODO PRO)**\n🕒 Hora EST sincronizada: {hora_actual}\n📅 Eventos: 10:00, 10:40, 11:10")

    for hora in noticias:
        # Alerta 10 min antes
        t_pre = (datetime.strptime(hora, "%H:%M") - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_pre).do(enviar_telegram, f"📢 **ALERTA INSTITUCIONAL:** Proyección de volatilidad en 10 min ({hora} EST).")
        
        # Punto Cero 2 min antes
        t_pos = (datetime.strptime(hora, "%H:%M") - timedelta(minutes=2)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(protocolo_posicionamiento, hora)

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    iniciar_cronograma()
    while True:
        # El loop usa la hora del sistema pero los 'at()' coinciden con la zona EST
        schedule.run_pending()
        time.sleep(15)
        
