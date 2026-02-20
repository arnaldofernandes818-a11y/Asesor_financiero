import requests
import schedule
import time
import os
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

# ==========================================
# CONFIGURACIÓN DE CONECTIVIDAD PRO
# ==========================================
TOKEN = "8138438253:AAGgdSgL67Kt1a0gEcm5NqYedsHKsa9UjN0"
CHAT_ID = "7100105540"

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
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT", timeout=5).json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5).json()
        return float(r_eur['price']), float(r_oro['price'])
    except:
        return None, None

def es_horario_bloqueo():
    # Bloqueo operativo de 5 AM a 7 AM EST para la cuenta, no para el simulador
    ahora = datetime.now()
    return 5 <= ahora.hour < 7

def ejecutar_analisis_latigazo(precio_base_eur, precio_base_oro, hora_evento):
    # ADN de la Estrategia: 120 segundos de espera para confirmar absorción
    time.sleep(120) 
    precio_final_eur, precio_final_oro = obtener_precios()
    
    if precio_final_eur and precio_base_eur:
        var_eur = ((precio_final_eur - precio_base_eur) / precio_base_eur) * 100
        var_oro = ((precio_final_oro - precio_base_oro) / precio_base_oro) * 100
        
        # Lógica de Veredicto Profesional
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

def protocolo_posicionamiento(hora):
    if es_horario_bloqueo():
        return # Silencio operativo durante el bloqueo de seguridad

    p_eur, p_oro = obtener_precios()
    
    if p_eur and p_oro:
        # Confirmación silenciosa de Punto Cero para no saturar el chat
        Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()
    else:
        enviar_telegram(f"⚠️ **SISTEMA:** Error de enlace con servidores de datos para el evento de las {hora}.")

# ==========================================
# CRONOGRAMA OPERATIVO DEFINITIVO
# ==========================================

def iniciar_cronograma():
    # Horarios Institucionales Reales
    noticias = ["08:41", "10:01", "14:31"]
    
    for hora in noticias:
        hora_dt = datetime.strptime(hora, "%H:%M")
        
        # Captura de Punto Cero (2 minutos antes de la noticia)
        t_pos = (hora_dt - timedelta(minutes=2)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(protocolo_posicionamiento, hora)
        
        # Alerta Preventiva Profesional
        t_pre = (hora_dt - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_pre).do(enviar_telegram, f"📢 **ALERTA INSTITUCIONAL:** Proyección de volatilidad en 10 minutos ({hora} EST).")

    # Mensaje de inicio profesional
    mensaje_inicio = (
        f"🏛️ **LACER PRO DUAL INTELLIGENCE**\n"
        f"✅ Núcleo de Análisis: ACTIVO\n"
        f"📡 Vigilancia de Liquidez: SINCRONIZADA\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 Noticieros programados para hoy (EST):\n"
        f"• 08:31 | 10:01 | 14:31\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💼 *Operativa bajo protocolos de riesgo dinámico.*"
    )
    enviar_telegram(mensaje_inicio)

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    iniciar_cronograma()
    while True:
        schedule.run_pending()
        time.sleep(15)
        
