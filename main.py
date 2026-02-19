import requests
import schedule
import time
import os
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

# ==========================================
# CONFIGURACIÓN DE CONECTIVIDAD
# ==========================================
TOKEN = "8138438253:AAGgdSgL67Kt1a0gEcm5NqYedsHKsa9UjN0"
CHAT_ID = "7100105540"

# --- BLOQUE DE COMPATIBILIDAD CON RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🏛️ LACER DUAL INTELLIGENCE: ACTIVO"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# -------------------------------------------

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        print("Error: Revisa tu conexión a internet.")

def obtener_precios():
    try:
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT").json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT").json()
        return float(r_eur['price']), float(r_oro['price'])
    except:
        return None, None

def ejecutar_analisis_latigazo(precio_base_eur, precio_base_oro, hora_evento):
    time.sleep(120) 
    precio_final_eur, precio_final_oro = obtener_precios()
    
    if precio_final_eur and precio_base_eur:
        var_eur = ((precio_final_eur - precio_base_eur) / precio_base_eur) * 100
        var_oro = ((precio_final_oro - precio_base_oro) / precio_base_oro) * 100
        
        v_eur = "🟢 FORTALECIMIENTO" if var_eur > 0.02 else "🔴 DEBILITAMIENTO" if var_eur < -0.02 else "⚖️ NEUTRO"
        v_oro = "🟢 FORTALECIMIENTO" if var_oro > 0.05 else "🔴 DEBILITAMIENTO" if var_oro < -0.05 else "⚖️ NEUTRO"

        mensaje = (
            f"🏛️ **VEREDICTO POST-NOTICIA**\n"
            f"⏱️ Evento: {hora_evento}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🇪🇺 **EURUSD (Euro)**\n"
            f"🔸 Impacto: {v_eur}\n"
            f"🔸 Variación: {var_eur:+.4f}%\n\n"
            f"🏆 **XAUUSD (Oro)**\n"
            f"🔸 Impacto: {v_oro}\n"
            f"🔸 Variación: {var_oro:+.4f}%\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 *Análisis de flujo de órdenes completado.*"
        )
        enviar_telegram(mensaje)

def protocolo_posicionamiento(hora):
    p_eur, p_oro = obtener_precios()
    enviar_telegram(f"⚖️ **SISTEMA EN POSICIÓN**\nSincronizando precios pre-noticia para las {hora}...")
    Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()

def iniciar_cronograma():
    schedule.every().day.at("02:00").do(enviar_telegram, "🌍 **LONDRES SESSION:** Vigilancia de volatilidad institucional activa.")

    noticias = ["08:31", "10:01", "14:31"]
    
    for hora in noticias:
        hora_dt = datetime.strptime(hora, "%H:%M")
        t_pos = (hora_dt - timedelta(minutes=1)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(protocolo_posicionamiento, hora)
        
        t_pre = (hora_dt - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_pre).do(enviar_telegram, f"⚠️ **NOTICIA PRÓXIMA:** 10 minutos para el evento de las {hora}.")

    print(">>> LACER INTELLIGENCE: DESPLEGADO")
    enviar_telegram("🏛️ **LACER DUAL INTELLIGENCE**\nSistemas de análisis fundamental y latigazos activos.")

if __name__ == "__main__":
    # Iniciar servidor web para que Render no mate el proceso
    Thread(target=run_web_server).start()
    
    # Iniciar lógica del bot
    iniciar_cronograma()
    while True:
        schedule.run_pending()
        time.sleep(30)
        
