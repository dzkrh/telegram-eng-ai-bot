import logging
import requests
from googletrans import Translator
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

logging.basicConfig(level=logging.INFO)
translator = Translator()

# Fungsi untuk menangani pesan
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text  # Pesan dari pengguna
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": user_msg}

    # Mengirimkan request ke Hugging Face API untuk mendapatkan respons
    response = requests.post(
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        headers=headers,
        json=payload
    )

    data = response.json()
    reply = data[0]["generated_text"] if isinstance(data, list) else "Sorry, something went wrong."

    # Terjemahkan reply dari bahasa Inggris ke bahasa Indonesia
    translated = translator.translate(reply, src="en", dest="id").text

    # Gabungkan reply asli dan terjemahannya
    full_reply = f"{reply}\n\n({translated})"

    # Kirimkan balasan ke pengguna dengan format dua bahasa
    await update.message.reply_text(full_reply)

# Set up bot dan handler
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Mulai bot
app.run_polling()