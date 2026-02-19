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

app = Flask(__name__)

@app.route('/')
def home():
    # Evita el error "Output too large" detectado en logs
    return "Lacer Pro: Online y Vigilando"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# FUNCIONES DE SEGURIDAD Y PRECIOS
# ==========================================

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        print("Error de red en Telegram")

def obtener_precios():
    # Optimización para arranque en caliente
    try:
        r_eur = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT", timeout=5).json()
        r_oro = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5).json()
        return float(r_eur['price']), float(r_oro['price'])
    except Exception as e:
        print(f"Error Binance: {e}")
        return None, None

def es_horario_bloqueo():
    # Bloqueo de 5 AM a 7 AM EST (Solo operativo, no para el simulador)
    ahora = datetime.now()
    return 5 <= ahora.hour < 7

# ==========================================
# LÓGICA DE ANÁLISIS (LATIGAZO)
# ==========================================

def ejecutar_analisis_latigazo(precio_base_eur, precio_base_oro, hora_evento):
    # Espera los 120 segundos del ADN de la estrategia
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
    else:
        enviar_telegram("⚠️ **FALLO DE ANÁLISIS:** Conexión perdida durante el latigazo.")

def protocolo_posicionamiento(hora):
    if es_horario_bloqueo():
        enviar_telegram(f"🛡️ **SEGURIDAD:** Noticia de las {hora} ignorada (Bloqueo 5-7 AM).")
        return

    p_eur, p_oro = obtener_precios()
    
    if p_eur and p_oro:
        # Confirmación de que el bot despertó a tiempo
        enviar_telegram(f"✅ **PUNTO CERO ALCANZADO**\nSincronización exitosa para las {hora}.\nAnalizando movimiento...")
        Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()
    else:
        # Diagnóstico de despertar tardío
        enviar_telegram(f"⚠️ **ALERTA:** El bot despertó para las {hora} pero Binance no respondió. Reintentando...")
        time.sleep(5)
        p_eur, p_oro = obtener_precios()
        if p_eur:
            Thread(target=ejecutar_analisis_latigazo, args=(p_eur, p_oro, hora)).start()

def iniciar_cronograma():
    # HORARIOS DE PRUEBA SOLICITADOS (Formato 24h)
    noticias = ["16:40", "17:15", "17:55"]
    
    for hora in noticias:
        hora_dt = datetime.strptime(hora, "%H:%M")
        
        # Sincroniza 2 minutos antes para asegurar que Render esté "caliente"
        t_pos = (hora_dt - timedelta(minutes=2)).strftime("%H:%M")
        schedule.every().day.at(t_pos).do(protocolo_posicionamiento, hora)
        
        # Aviso preventivo 10 minutos antes
        t_pre = (hora_dt - timedelta(minutes=10)).strftime("%H:%M")
        schedule.every().day.at(t_pre).do(enviar_telegram, f"⚠️ **NOTICIA PRÓXIMA:** 10 min para las {hora}.")

    enviar_telegram("🏛️ **SISTEMA DE PRUEBA ONLINE**\nEsperando horarios: 4:40PM, 5:15PM y 5:55PM.")

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    iniciar_cronograma()
    while True:
        schedule.run_pending()
        time.sleep(15) 
    
