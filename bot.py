import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def run_bot():

    bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Bot funcionando correctamente"
    )

    while True:
        # mensaje de prueba cada 30 minutos
        bot.send_message(
            chat_id=CHAT_ID,
            text="🤖 Bot activo y funcionando"
        )
        time.sleep(1800)

# servidor web para Render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot running')

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

run_bot()
