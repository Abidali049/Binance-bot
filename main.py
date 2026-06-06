import re
import asyncio
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = 27394279
API_HASH = "90a9aa4c31afa3750da5fd686c410851"
SESSION_TOKEN = "1BJWap1sBuycDCcg9T0yI1BNq4870KCssRs29tu6KfVf_Jin4M7H8QeTUZcQmSgEVhTqtbMrJDKqRLIXHRHxDPkS3vzYbDkY0_UKVVR7YTwyy26jgNOcnPZiI2Ph2Bn-j81m9ArKHK_xVDvY-9K2v_XN1I76Ms1nE5HsQGPzs9GOfKwl215H4J-8QaxByXN1vLSPvVrasAz6Ar8bbU_mbXOh_djYSbkZt-d74Q6TktwfmfXJxhm4obxqHjxgoFE5IJlrfobFJ_S7iZL8asN-43zK_-KrTiQK1s7aJ7HGYs6KXTAEmQ0vossn1RzXTRAonDkoA1i9A0n0kGywe5JBf_EP7S2xJe5U="

SOURCE_IDS = [-1002018715164, -1001932975551, -1002439510384, -1001748979180, -1002189568137]
DEST_CHANNELS = [-1003999599055, -1002543030366, -1003946282744]

client = TelegramClient(StringSession(SESSION_TOKEN), API_ID, API_HASH, connection_retries=None, auto_reconnect=True)

@client.on(events.NewMessage(chats=SOURCE_IDS))
async def handler(event):
    try:
        content = event.message.message or ""
        codes = re.findall(r'\b[A-Z0-9]{7,10}\b', content)
        for code in codes:
            if code not in ["BINANCE", "CLAIM", "FREE", "JOIN"]:
                msg = f"<code>{code}</code>"
                for dest_id in DEST_CHANNELS:
                    try:
                        await client.send_message(dest_id, msg, parse_mode='html')
                        print(f"🔥 FORWARDED: {code}")
                    except:
                        pass
    except:
        pass

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot Active")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

async def main():
    threading.Thread(run_health_server, daemon=True).start()
    await client.start()
    print("🚀 BOT IS ONLINE ON RENDER!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
