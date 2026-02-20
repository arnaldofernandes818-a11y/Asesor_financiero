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
    # Retorno simple para evitar saturación de logs en Render
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
# NÚCLEO DE INTELIGENCIA DE DATOS (SIN BLOQUEOS)
# ==========================================

def obtener_precios():
    # Captura rápida para asegurar el Punto Cero
    try:
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT", timeout=5).json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5).json()
        return float(r_eur['price']), float(r_oro['price'])
    except:
        return None, None

def ejecutar_analisis_latigazo(precio_base_eur, precio_base_oro, hora_evento):
    # ADN de la Estrategia: 120 segundos para confirmar la absorción del movimiento
    time.sleep(120) 
    precio_final_eur, precio_final_oro = obtener_precios()
    
    if precio_final_eur and precio_base_eur:
        var_eur = ((precio_final_eur - precio_base_eur) / precio_base_eur) * 100
        var_oro = ((precio_final_oro - precio_base_oro) / precio_base_oro) * 100
        
        # Veredictos basados en volatilidad institucional
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
    # Eliminada la restricción de 5-7 AM por orden del usuario
    p_eur, p_oro = obtener_precios()
    
    if p_eur and p_oro:
        # Registro del Punto Cero exitoso
        Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()
    else:
        enviar_telegram(f"⚠️ **SISTEMA:** Error de enlace con servidores para el evento de las {hora}.")

# ==========================================
# CRONOGRAMA OPERATIVO DEFINITIVO
# ==========================================

def iniciar_cronograma():
    # Horarios reales solicitados
    noticias = ["09:10", "10:01", "14:31"]
    
    for hora in noticias:
        hora_dt = datetime.strptime(hora, "%H:%M")
        
        # Sincronización 2 minutos antes para asegurar el encendido en Render
        t_pos = (hora_dt - timedelta(minutes=2)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(protocolo_posicionamiento, hora)
        
        # Alerta preventiva 10 minutos antes
        t_pre = (hora_dt - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_pre).do(enviar_telegram, f"📢 **ALERTA INSTITUCIONAL:** Proyección de volatilidad en 10 min ({hora} EST).")

    mensaje_inicio = (
        f"🏛️ **LACER PRO DUAL INTELLIGENCE**\n"
        f"✅ Núcleo de Análisis: ACTIVO\n"
        f"📡 Vigilancia de Liquidez: SINCRONIZADA\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 Noticieros programados para hoy (EST):\n"
        f"• 08:31 | 10:01 | 14:31\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💼 *Operativa institucional sin restricciones de horario.*"
    )
    enviar_telegram(mensaje_inicio)

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    iniciar_cronograma()
    while True:
        schedule.run_pending()
        time.sleep(15)
    
