import requests
import schedule
import time
import pytz
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN INSTITUCIONAL ---
TOKEN = "8138438253:AAGgdSgL67Kt1a0gEcm5NqYedsHKsa9UjN0"
CHAT_ID = "7100105540"
COLOMBIA_TZ = pytz.timezone('America/Bogota')

app = Flask('')

@app.route('/')
def home():
    return "Lacer Cloud Intelligence - Active Terminal"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        pass

def obtener_precios():
    try:
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT").json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT").json()
        return float(r_eur['price']), float(r_oro['price'])
    except:
        return None, None

def analizar_impacto_real(p_base_eur, p_base_oro, hora_noticia):
    time.sleep(120) 
    p_final_eur, p_final_oro = obtener_precios()
    
    if p_final_eur and p_base_eur:
        var_eur = ((p_final_eur - p_base_eur) / p_base_eur) * 100
        var_oro = ((p_final_oro - p_base_oro) / p_base_oro) * 100
        
        v_eur = "🔹 ALCISTA" if var_eur > 0.02 else "🔸 BAJISTA" if var_eur < -0.02 else "⚖️ LATERAL"
        v_oro = "🔹 ALCISTA" if var_oro > 0.05 else "🔸 BAJISTA" if var_oro < -0.05 else "⚖️ LATERAL"

        mensaje = (
            f"🏛️ **LACER CLOUD INTELLIGENCE**\n"
            f"📊 **INFORME DE VOLATILIDAD**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱️ **Evento:** {hora_noticia}\n"
            f"🌍 **Impacto EURUSD:** {v_eur} ({var_eur:+.4f}%)\n"
            f"🏆 **Impacto XAUUSD:** {v_oro} ({var_oro:+.4f}%)\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 *Veredicto de flujo institucional completado.*"
        )
        enviar_telegram(mensaje)

def posicionar_sistema(hora):
    p_eur, p_oro = obtener_precios()
    enviar_telegram(f"⚖️ **SISTEMA EN POSICIÓN**\nCapturando métricas para la noticia de las {hora}...")
    Thread(target=analizar_impacto_real, args=(p_eur, p_oro, hora)).start()

def iniciar_cronograma():
    schedule.every().day.at("02:00").do(enviar_telegram, "🌍 **LONDRES:** Apertura detectada. Vigilancia institucional activa.")
    
    # --- CAMBIA LAS HORAS AQUÍ (SOLO UNA VEZ) ---
    noticias = ["07:00", "08:30", "13:00"] 
    
    for hora in noticias:
        hora_dt = datetime.strptime(hora, "%H:%M")
        
        # El bot calcula automáticamente el aviso de 5 min antes
        t_aviso = (hora_dt - timedelta(minutes=5)).strftime("%H:%M")
        schedule.every().day.at(t_aviso).do(enviar_telegram, f"⚠️ **AVISO PROFESIONAL:** 5 minutos para noticia de las {hora}.")
        
        # El bot calcula automáticamente el posicionamiento 1 min antes
        t_pos = (hora_dt - timedelta(minutes=1)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(posicionar_sistema, hora)

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    enviar_telegram("🏛️ **LACER CLOUD INTELLIGENCE**\n✅ Terminal operativo. Gestión de noticias sincronizada.")
    iniciar_cronograma()
    
    while True:
        schedule.run_pending()
        time.sleep(30)
