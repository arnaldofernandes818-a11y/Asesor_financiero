import requests
import schedule
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Lacer Cloud Intelligence Online"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- CONFIGURACIÓN DE TELEGRAM ---
TOKEN = "8138438253:AAGgdSgL67Kt1a0gEcm5NqYedsHKsa9UjN0"
CHAT_ID = "7100105540"

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try: requests.post(url, data=payload)
    except: pass

def obtener_precios():
    try:
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT").json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT").json()
        return float(r_eur['price']), float(r_oro['price'])
    except: return None, None

def analizar_impacto_real(p_base_eur, p_base_oro, hora_noticia):
    # El bot espera 2 minutos para ver la reacción real del mercado
    time.sleep(120) 
    p_final_eur, p_final_oro = obtener_precios()
    
    if p_final_eur and p_base_eur:
        var_eur = ((p_final_eur - p_base_eur) / p_base_eur) * 100
        var_oro = ((p_final_oro - p_base_oro) / p_base_oro) * 100
        
        v_eur = "🟢 FORTALECIMIENTO" if var_eur > 0.02 else "🔴 DEBILITAMIENTO" if var_eur < -0.02 else "⚖️ NEUTRO"
        v_oro = "🟢 FORTALECIMIENTO" if var_oro > 0.05 else "🔴 DEBILITAMIENTO" if var_oro < -0.05 else "⚖️ NEUTRO"

        mensaje = (
            f"🏛️ **VEREDICTO POST-NOTICIA**\n"
            f"⏱️ Evento: {hora_noticia}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🇪🇺 **EURUSD:** {v_eur} ({var_eur:+.4f}%)\n"
            f"🏆 **XAUUSD:** {v_oro} ({var_oro:+.4f}%)\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 *Análisis de flujo de órdenes completado.*"
        )
        enviar_telegram(mensaje)

def posicionar_sistema(hora):
    p_eur, p_oro = obtener_precios()
    enviar_telegram(f"⚖️ **SISTEMA EN POSICIÓN (CLOUD)**\nCapturando métricas pre-noticia ({hora})...")
    Thread(target=analizar_impacto_real, args=(p_eur, p_oro, hora)).start()

def iniciar_cronograma():
    # 1. Apertura de Londres
    schedule.every().day.at("02:00").do(enviar_telegram, "🌍 **LONDRES:** Vigilancia institucional activa.")
    
    # 2. LISTA DE NOTICIAS (Ajusta estas horas cada mañana)
    noticias = ["08:31", "10:01", "23:48"] 
    
    for hora in noticias:
        hora_dt = datetime.strptime(hora, "%H:%M")
        t_pos = (hora_dt - timedelta(minutes=1)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(posicionar_sistema, hora)
        
        t_aviso = (hora_dt - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_aviso).do(enviar_telegram, f"⚠️ **AVISO:** 10 min para noticia de las {hora}.")

if __name__ == "__main__":
    # Iniciar servidor web y cronograma
    Thread(target=run_web_server).start()
    iniciar_cronograma()
    while True:
        schedule.run_pending()
        time.sleep(30)
        
