import telebot
import requests
import json
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import os
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. CARGA DE CONFIGURACIÓN
load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
url = os.getenv('API_URL')

if not token or not url:
    print("Error: No se encontró la configuración. Ejecuta primero 'python config.py'")
    exit()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

bot = telebot.TeleBot(token)
print("Bot de Telegram iniciado. Esperando mensajes...")

cache_fuentes = {}


@bot.message_handler(func=lambda message: True)
def contro_mensaje(mensaje):
    pregunta = mensaje.text
    chat_id = mensaje.chat.id

    msg_espera = bot.reply_to(mensaje, "espera...")

    payload = {
        "pregunta": pregunta,
        "historial": []
    }

    try:
        r_rag = requests.post(url, json=payload, stream=True)
        r_rag.raise_for_status()

        # Recopilar toda la respuesta cruda primero para no romper el JSON
        respuesta_cruda = ""
        for chunk in r_rag.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                respuesta_cruda += chunk

        texto_fin = ""
        fuentes_texto = ""

        if "<<<META_START>>>" in respuesta_cruda and "<<<META_END>>>" in respuesta_cruda:
            partes = respuesta_cruda.split("<<<META_END>>>")
            meta_raw = partes[0].replace("<<<META_START>>>", "").strip()
            texto_fin = partes[1].strip()

            try:
                meta_d = json.loads(meta_raw)
                if meta_d.get("tipo") == "rag":
                    fuentes = meta_d.get("fuentes", [])
                    if fuentes:
                        paginas = sorted(list(set(str(f["pagina"]) for f in fuentes)))
                        fuentes_texto = f"\n\n*DP-800 recursos :* pagina {', '.join(paginas)}"
            except json.JSONDecodeError:
                pass
        else:
            texto_fin = respuesta_cruda.strip()

        respuesta_principal = texto_fin
        MAX_LONG = 4000

        markup = None
        if fuentes_texto:
            cache_fuentes[str(msg_espera.message_id)] = fuentes_texto
            markup = InlineKeyboardMarkup()
            btn = InlineKeyboardButton("Mostar recursos", callback_data=f"fuentes_{msg_espera.message_id}")
            markup.add(btn)

        if len(respuesta_principal) <= MAX_LONG:
            bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id, text=respuesta_principal,
                                  reply_markup=markup)
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id,
                                  text=respuesta_principal[:MAX_LONG])
            for i in range(MAX_LONG, len(respuesta_principal), MAX_LONG):
                chunk_str = respuesta_principal[i:i + MAX_LONG]
                if i + MAX_LONG >= len(respuesta_principal):
                    bot.send_message(chat_id, chunk_str, reply_markup=markup)
                else:
                    bot.send_message(chat_id, chunk_str)

    except requests.exceptions.ConnectionError:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id, text="La api no responde revisa el token o la url..")
    except Exception as e:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id, text=f"Error: {str(e)}")


@bot.message_handler(content_types=['photo'])
def manejar_imagen(message):
    chat_id = message.chat.id
    msg_espera = bot.reply_to(message, "Aplicando filtros y extrayendo el texto")

    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        img_descargada = requests.get(f"https://api.telegram.org/file/bot{token}/{file_info.file_path}")

        imagen = Image.open(io.BytesIO(img_descargada.content))

        imagen = imagen.convert('L')
        enhancer = ImageEnhance.Contrast(imagen)
        imagen = enhancer.enhance(2.0)
        imagen = imagen.filter(ImageFilter.SHARPEN)

        configuracion_ocr = r'--psm 6'
        texto_extraido = pytesseract.image_to_string(imagen, lang='eng', config=configuracion_ocr).strip()

        print(f"\n--- TEXTO EXTRAÍDO POR TESSERACT ---\n{texto_extraido}\n------------------------------------\n")

        if not texto_extraido:
            bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id,
                                  text="No a sido posible realizar la estracion por TESSERACT.")
            return

        bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id,
                              text="Enviando el texto a sql server")

        payload_rag = {
            "pregunta": texto_extraido,
            "historial": []
        }

        r_rag = requests.post(url, json=payload_rag, stream=True)
        r_rag.raise_for_status()

        respuesta_cruda = ""
        for chunk in r_rag.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                respuesta_cruda += chunk

        texto_fin = ""
        fuentes_texto = ""

        if "<<<META_START>>>" in respuesta_cruda and "<<<META_END>>>" in respuesta_cruda:
            partes = respuesta_cruda.split("<<<META_END>>>")
            meta_raw = partes[0].replace("<<<META_START>>>", "").strip()
            texto_fin = partes[1].strip()

            try:
                meta_d = json.loads(meta_raw)
                if meta_d.get("tipo") == "rag":
                    fuentes = meta_d.get("fuentes", [])
                    if fuentes:
                        paginas = sorted(list(set(str(f["pagina"]) for f in fuentes)))
                        fuentes_texto = f"\n\n*DP-800 recursos :* Pagina {', '.join(paginas)}"
            except json.JSONDecodeError:
                pass
        else:
            texto_fin = respuesta_cruda.strip()

        respuesta_principal = texto_fin
        MAX_LONG = 4000

        markup = None
        if fuentes_texto:
            cache_fuentes[str(msg_espera.message_id)] = fuentes_texto
            markup = InlineKeyboardMarkup()
            btn = InlineKeyboardButton("Ver fuentes", callback_data=f"fuentes_{msg_espera.message_id}")
            markup.add(btn)

        # Enviar respuesta y evitar el error 400
        if len(respuesta_principal) <= MAX_LONG:
            bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id, text=respuesta_principal,
                                  reply_markup=markup)
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id,
                                  text=respuesta_principal[:MAX_LONG])
            for i in range(MAX_LONG, len(respuesta_principal), MAX_LONG):
                chunk_str = respuesta_principal[i:i + MAX_LONG]
                if i + MAX_LONG >= len(respuesta_principal):
                    bot.send_message(chat_id, chunk_str, reply_markup=markup)
                else:
                    bot.send_message(chat_id, chunk_str)

    except requests.exceptions.ConnectionError:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id, text="Error la api no responde")
    except Exception as e:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_espera.message_id, text=f"Error al procesar: {str(e)}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('fuentes_'))
def mostrar_fuentes(call):
    msg_id = call.data.split('_')[1]
    fuentes = cache_fuentes.get(msg_id, "El recurso no se encuentra disponible")

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, fuentes, reply_to_message_id=call.message.message_id, parse_mode="Markdown")


bot.polling(none_stop=True)