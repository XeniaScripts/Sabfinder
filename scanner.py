import requests
import os

# --- SETTINGS ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1467943822712639570/KdCEMFFmMmIiWXQvuoybwOH-A0T2wDOpp1mC5szqvN56PPnWwzL0DQc636UEDGDs7335"
PLACE_ID = "15502339080"  # Example: Pet Sim 99 (Change this to your game ID)

def scan_all_servers():
    cursor = ""
    print(f"🔍 Scanning all servers for PlaceID: {PLACE_ID}")
    
    # We scan multiple pages of the server list (up to 500 servers per run)
    for _ in range(5):
        url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100&cursor={cursor}"
        try:
            res = requests.get(url).json()
            if "data" not in res: break
            
            for server in res["data"]:
                # WHALE LOGIC: 
                # Servers with exactly 1 slot left or full are usually the most valuable.
                if server["playing"] >= (server["maxPlayers"] - 1):
                    job_id = server["id"]
                    ping_webhook(server["playing"], job_id)
            
            cursor = res.get("nextPageCursor")
            if not cursor: break
        except:
            break

def ping_webhook(players, job_id):
    join_link = f"https://www.roblox.com/games/{PLACE_ID}?jobId={job_id}"
    data = {
        "content": "🐋 **WHALE SERVER DETECTED**",
        "embeds": [{
            "title": f"Target Server: {players} Players",
            "description": "High-value activity detected in this server instance.",
            "color": 0x00ffff,
            "fields": [
                {"name": "🔗 Quick Join", "value": f"**[CLICK TO JOIN]({join_link})**"}
            ],
            "footer": {"text": "Xenia Global Scanner | 24/7 Cloud Monitoring"}
        }]
    }
    requests.post(WEBHOOK_URL, json=data)

if __name__ == "__main__":
    scan_all_servers()
