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
# Datos extraídos de tu configuración de Lacer Pro
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
    # Obtenemos la fecha actual en la zona horaria de NY (EST)
    ahora = datetime.now(ZONA_HORARIA)
    hoy_str = ahora.strftime("%Y-%m-%d")
    dia_semana = ahora.weekday()  # 0=Lunes, 6=Domingo
    
    # Detección técnica de último viernes de mes (Rebalanceo)
    es_ultimo_viernes = (dia_semana == 4 and (ahora.day + 7) > 31)
    
    # --- LÓGICA DE DECISIÓN INSTITUCIONAL ---
    
    # 1. Caso Festivo (Mercado Cerrado)
    if hoy_str in FESTIVOS_2026:
        msg = (f"🏛️ **WALL STREET ESTRATEGIC REPORT**\n"
               f"📅 {hoy_str} | **Status:** 🔴 **NO OPERAR**\n\n"
               f"**ALERTA INSTITUCIONAL:**\n"
               f"El mercado está en pausa por: {FESTIVOS_2026[hoy_str]}. "
               f"Bancos centrales y proveedores de liquidez fuera de servicio.\n\n"
               f"**DIAGNÓSTICO:**\n"
               f"Cualquier movimiento es ruido minorista sin respaldo de capital real.\n\n"
               f"**RECOMENDACIÓN:** Abstención total. Disfruta tu día libre.")

    # 2. Caso Fin de Semana
    elif dia_semana >= 5:
        return # Silencio total en fin de semana

    # 3. Caso Precaución (Baja Liquidez o Periodos de Transición)
    elif es_ultimo_viernes or (ahora.month == 12 and ahora.day >= 20) or (ahora.month == 1 and ahora.day <= 5):
        motivo = "Cierre de Mes / Rebalanceo Institucional" if es_ultimo_viernes else "Periodo de Vacaciones de Invierno"
        msg = (f"🏛️ **WALL STREET ESTRATEGIC REPORT**\n"
               f"📅 {hoy_str} | **Status:** ⚠️ **PRECAUCIÓN PROFESIONAL**\n\n"
               f"**ANÁLISIS DE CONTEXTO:**\n"
               f"Fase de {motivo}. El volumen de los Market Makers está disminuyendo.\n\n"
               f"**ADVERTENCIA TÉCNICA:**\n"
               f"Riesgo de volatilidad errática. El mercado podría ignorar niveles técnicos básicos.\n\n"
               f"**RECOMENDACIÓN:** Reduce el riesgo al 50%. Preserva tu capital.")

    # 4. Caso Día Operativo (Luz Verde)
    else:
        msg = (f"🏛️ **WALL STREET ESTRATEGIC REPORT**\n"
               f"📅 {hoy_str} | **Status:** 🟢 **OPERATIVO**\n\n"
               f"**ANÁLISIS DE APERTURA LONDRES:**\n"
               f"Plazas de Londres (LSE) y Nueva York (NYSE) operativas. Flujo de órdenes estabilizado.\n\n"
               f"**PERSPECTIVA:**\n"
               f"Estructura óptima para ejecución profesional. Sin interferencias bancarias.\n\n"
               f"**RECOMENDACIÓN:** Riesgo 100% autorizado. ¡Buen trading!")

    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

# --- MOTOR DE TIEMPO (PROGRAMADO A LAS 02:00 AM EST) ---
def runner():
    # Programado para las 02:00 AM NY (Apertura de Londres)
    schedule.every().day.at("02:00").do(enviar_reporte_diario)
    while True:
        schedule.run_pending()
        time.sleep(30)

# --- SERVIDOR FLASK (INTERFAZ PARA RENDER) ---
@app.route('/')
def home():
    return "🏛️ WALL STREET INTELLIGENCE: CENTRAL OPERATIONS - ONLINE"

if __name__ == "__main__":
    # Iniciamos el hilo del cronograma para que corra en paralelo
    t = Thread(target=runner)
    t.daemon = True
    t.start()
    
    # Ejecutamos el servidor web
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
