import requests
import time
import os
from telegram import Bot

# VARIABLES DE ENTORNO
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)

headers = {
    "x-apisports-key": API_KEY
}

alerted_matches = set()

def check_matches():

    url = "https://v3.football.api-sports.io/fixtures?live=all"
    response = requests.get(url, headers=headers)
    data = response.json()

    for match in data["response"]:

        fixture_id = match["fixture"]["id"]
        minute = match["fixture"]["status"]["elapsed"]

        if minute is None:
            continue

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        goals_home = match["goals"]["home"] or 0
        goals_away = match["goals"]["away"] or 0
        total_goals = goals_home + goals_away

        stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
        stats_response = requests.get(stats_url, headers=headers)
        stats = stats_response.json()

        try:

            home_stats = stats["response"][0]["statistics"]
            away_stats = stats["response"][1]["statistics"]

            shots_home = home_stats[2]["value"] or 0
            shots_away = away_stats[2]["value"] or 0

            shots_target_home = home_stats[0]["value"] or 0
            shots_target_away = away_stats[0]["value"] or 0

            attacks_home = home_stats[13]["value"] or 0
            attacks_away = away_stats[13]["value"] or 0

            total_shots = shots_home + shots_away
            total_target = shots_target_home + shots_target_away
            total_attacks = attacks_home + attacks_away

        except:
            continue

        if (
            15 <= minute <= 45
            and total_goals == 0
            and total_shots >= 8
            and total_target >= 3
            and total_attacks >= 20
            and fixture_id not in alerted_matches
        ):

            message = f"""
⚽ POSIBLE GOL 1ª PARTE

{home} vs {away}

Minuto: {minute}

Tiros: {total_shots}
Tiros a puerta: {total_target}
Ataques peligrosos: {total_attacks}

Probable Over 0.5 HT
"""

            bot.send_message(chat_id=CHAT_ID, text=message)

            alerted_matches.add(fixture_id)

def run_bot():

    while True:
        try:
            check_matches()
        except Exception as e:
            print("Error:", e)

        time.sleep(60)

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot running')

def run_server():
    port = 10000
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

run_bot()
