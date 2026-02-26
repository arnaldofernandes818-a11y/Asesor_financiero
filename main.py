import telebot
import schedule
import time
import os
import pytz
from datetime import datetime
from threading import Thread
from flask import Flask

# ==========================================
# CONFIGURACIÓN PROFESIONAL (CREDENTIALS)
# ==========================================
TOKEN = "8138438253:AAGgdSgL67Kt1a0gEcm5NqYedsHKsa9UjN0"
CHAT_ID = "7100105540"
ZONA_HORARIA = pytz.timezone('US/Eastern')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ==========================================
# BASE DE DATOS DE CALENDARIO 2026 (ADN)
# ==========================================
FESTIVOS_2026 = {
    "2026-01-01": "Año Nuevo (Global)",
    "2026-01-19": "Martin Luther King Jr. Day (USA)",
    "2026-02-16": "Presidents' Day (USA)",
    "2026-04-03": "Viernes Santo (USA/UK)",
    "2026-04-06": "Lunes de Pascua (UK)",
    "2026-05-04": "Early May Bank Holiday (UK)",
    "2026-05-25": "Memorial Day (USA) / Spring Bank Holiday (UK)",
    "2026-06-19": "Juneteenth (USA)",
    "2026-07-03": "Independencia de USA (Obs.)",
    "2026-08-31": "Summer Bank Holiday (UK)",
    "2026-09-07": "Labor Day (USA)",
    "2026-11-26": "Thanksgiving Day (USA)",
    "2026-12-25": "Navidad (Global)",
    "2026-12-28": "Boxing Day (UK - Obs.)"
}

def enviar_reporte_diario():
    ahora = datetime.now(ZONA_HORARIA)
    hoy_str = ahora.strftime("%Y-%m-%d")
    dia_semana = ahora.weekday()
    es_ultimo_viernes = (dia_semana == 4 and (ahora.day + 7) > 31)
    
    if hoy_str in FESTIVOS_2026:
        msg = (f"🏛️ **WALL STREET ESTRATEGIC REPORT**\n"
               f"📅 {hoy_str} | **Status:** 🔴 **NO OPERAR**\n\n"
               f"**ALERTA INSTITUCIONAL:**\n"
               f"El mercado está en pausa por: {FESTIVOS_2026[hoy_str]}.\n\n"
               f"**RECOMENDACIÓN:** Abstención total. Disfruta tu día libre.")
    elif dia_semana >= 5:
        return
    elif es_ultimo_viernes or (ahora.month == 12 and ahora.day >= 20) or (ahora.month == 1 and ahora.day <= 5):
        motivo = "Cierre de Mes / Rebalanceo Institucional" if es_ultimo_viernes else "Periodo de Vacaciones de Invierno"
        msg = (f"🏛️ **WALL STREET ESTRATEGIC REPORT**\n"
               f"📅 {hoy_str} | **Status:** ⚠️ **PRECAUCIÓN PROFESIONAL**\n\n"
               f"**ANÁLISIS DE CONTEXTO:**\n"
               f"Fase de {motivo}.\n\n"
               f"**RECOMENDACIÓN:** Reduce el riesgo al 50%. Preserva tu capital.")
    else:
        msg = (f"🏛️ **WALL STREET ESTRATEGIC REPORT**\n"
               f"📅 {hoy_str} | **Status:** 🟢 **OPERATIVO**\n\n"
               f"**ANÁLISIS DE APERTURA LONDRES:**\n"
               f"Plazas operativas. Flujo de órdenes estabilizado.\n\n"
               f"**RECOMENDACIÓN:** Riesgo 100% autorizado. ¡Buen trading!")

    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

def runner():
    schedule.every().day.at("02:00").do(enviar_reporte_diario)
    while True:
        schedule.run_pending()
        time.sleep(30)

@app.route('/')
def home():
    return "🏛️ WALL STREET INTELLIGENCE: CENTRAL OPERATIONS - ONLINE"

if __name__ == "__main__":
    t = Thread(target=runner)
    t.daemon = True
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
