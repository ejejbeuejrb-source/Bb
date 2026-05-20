import requests
import time
import threading
from datetime import datetime

# ============================================================
#  CONFIG
# ============================================================
ACCESS_TOKEN = "eyJhbGciOiJQUzI1NiIsImtpZCI6IkU1N1lkcnVIcGxBanUyY05vMURvckgzajI3QnU1LXNfT1A1UHdQaWhuNU0ifQ.eyJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpLnZpbnRlZC5jb20iLCJjbGllbnRfaWQiOiJ3ZWIiLCJleHAiOjE3NzkzMjQ3NjEsImlhdCI6MTc3OTI4MTU2MSwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwicHVycG9zZSI6ImFjY2VzcyIsInNjb3BlIjoicHVibGljIiwic2lkIjoiN2Y0MGEyYWQtMTc3OTI4MTU2MSJ9.DvQ3YEKF5Mfop5kd5Y0v69Ov2X-Gxl9aLCTh8MuvSuZn6x8kYKnxsk7E4njBhxiijz9HHeI7L-o-8zIGvxF1xwGby0YdmbSbP8cVInRkFyKAwMynBAXPpFLOyOSitU4VR0POoJIYcpps0ei1aI1g-lBbDm_uUWC-viXpxViuiIo-W7IS7myQ8qdVHWqY5LB9dcIgWR4Htj0P2Y-DLfpjL6Tk8KfXQKVDiDUqkU_AgctDVoNGoHNrak9RgL0d3xCLVVj7gjyr1xcY7N6tIfOu4DnwkqZq3kBdXerFtX0P5rXIynRhXpRb_0hGyvdQd1jL6yvLy9HE64uDPSxNTuFMzA"

CATEGORIES = [
    {
        "nom":      "RTX",
        "search":   "carte graphique RTX",
        "prix_min": 20,
        "prix_max": 600,
        "webhook":  "https://discordapp.com/api/webhooks/1504906470029004831/UWZKPXNYontdHqt6hMQe8jC4Qvo_Zgk4Zxeb8jE9qHl-vDE1tYX3siatNVSs_prLDYa7",
        "couleur":  0x3b82f6,
    },
    {
        "nom":      "switch",
        "search":   "Nintendo Switch Oled",
        "prix_min": 40,
        "prix_max": 90,
        "webhook":  "https://discord.com/api/webhooks/1506342542449311996/5CsPnlymqqqUTdArOfA7anl7sKaHG3FWj3SgYM8Zu7ER2UjpxwAVLeIz_ufE_PBDbJoU",
        "couleur":  0x3b82f6,
    },
    {
        "nom":      "PS5",
        "search":   "ps5",
        "prix_min": 130,
        "prix_max": 250,
        "webhook":  "https://discordapp.com/api/webhooks/1504970943859134525/sThKzDwI1gk94DyQWqjc6OffMBKPz-5mRRXrFoV6ukQFj-HFBJ92vyUD85Jo_KfqD6kB",
        "couleur":  0xf97316,
        "requis":   ["ps5", "playstation 5"],
        "blacklist": ["manette", "jeu", "cable", "chargeur", "support", "skin", "housse", "casque", "sacoche", "ventilateur", "dock", "facade"],
    },
    {
        "nom":      "Xbox Series S",
        "search":   "xbox series s",
        "prix_min": 50,
        "prix_max": 125,
        "webhook":  "https://discordapp.com/api/webhooks/1504971178576711740/A0NNMxWVlvlRrxmcSGuXjV_wr4ASGyvnDnVd_9sUfSXZNLDfxNVO20xw_7XjidE5QZMn",
        "couleur":  0x22c55e,
    },
    {
        "nom":      "PC Gamer",
        "search":   "pc gamer",
        "prix_min": 50,
        "prix_max": 600,
        "webhook":  "https://discordapp.com/api/webhooks/1504906008525406299/5QLm-6uRMRFtudSv5kHJgo1L7Xz3BMnkbahFprMZ1kx9iXfIeu8GCpcJvJAvgcqgiHnH",
        "couleur":  0x8b5cf6,
    },
    {
        "nom":      "Carte Mere",
        "search":   "carte mere motherboard",
        "prix_min": 0,
        "prix_max": 60,
        "webhook":  "https://discord.com/api/webhooks/1505678603294212176/4bpdgEDtuMTnr0FXUYCcLTn3waJYB-FhviVRlk7VcI5Cyic31wHrNSNZrPB4aFhZC1iz",
        "couleur":  0x10b981,
        "requis":   ["b450","x470","b550","x570","b650","x670","z490","z590","b460","b560","z690","z790","b660","b760"],
        "blacklist": ["pc complet", "pc gamer", "slot", "bracket", "equerre", "backplate", "radiateur"],
    },
    {
        "nom":      "Processeur",
        "search":   "processeur CPU",
        "prix_min": 0,
        "prix_max": 60,
        "webhook":  "https://discord.com/api/webhooks/1505677885191491775/3V9JhBp4JtZppBqdDgL0N-FJmgSm2CvrEJhO74Rkag8fmGNT6eoEyyT8UaSlFaqijgGv",
        "couleur":  0xef4444,
        "requis":   [
            "i3-9","i5-9","i7-9","i9-9",
            "i3-10","i5-10","i7-10","i9-10",
            "i3-11","i5-11","i7-11","i9-11",
            "i3-12","i5-12","i7-12","i9-12",
            "i3-13","i5-13","i7-13","i9-13",
            "i3-14","i5-14","i7-14","i9-14",
            "ryzen 5 3","ryzen 7 3","ryzen 9 3",
            "ryzen 5 5","ryzen 7 5","ryzen 9 5",
            "ryzen 5 7","ryzen 7 7","ryzen 9 7",
            "ryzen 5 9","ryzen 7 9","ryzen 9 9",
            "3600","3700x","3900x",
            "5600","5700x","5800x","5900x","5950x",
            "7600","7700x","7800x","7900x","7950x",
        ],
        "blacklist": ["ventilateur","ventirad","cooler","refroidisseur","pate","boite vide","carte mere","pc complet"],
    },
    {
        "nom":      "SSD NVMe 500Go",
        "search":   "ssd nvme 500go",
        "prix_min": 0,
        "prix_max": 20,
        "webhook":  "https://discord.com/api/webhooks/1505676803195404409/HegYZYu4m1hH1neGysoq4X-Nu2EAphEAiCQSlhaBFaYElJIqROCA4z7OxCjxutSjeQ1W",
        "couleur":  0xf59e0b,
        "requis":   ["500go","500gb","512go","512gb","480go","480gb"],
        "blacklist": ["1to","1tb","2to","2tb","sata","boitier","adaptateur","cable","support","portable","laptop"],
    },
    {
        "nom":      "SSD NVMe 1To",
        "search":   "ssd nvme 1to",
        "prix_min": 0,
        "prix_max": 35,
        "webhook":  "https://discord.com/api/webhooks/1505676803195404409/HegYZYu4m1hH1neGysoq4X-Nu2EAphEAiCQSlhaBFaYElJIqROCA4z7OxCjxutSjeQ1W",
        "couleur":  0xf59e0b,
        "requis":   ["1to","1tb","1 to","1 tb"],
        "blacklist": ["500go","500gb","512go","2to","2tb","sata","boitier","adaptateur","cable","support","portable","laptop"],
    },
    {
        "nom":      "SSD NVMe 2To",
        "search":   "ssd nvme 2to",
        "prix_min": 0,
        "prix_max": 60,
        "webhook":  "https://discord.com/api/webhooks/1505676803195404409/HegYZYu4m1hH1neGysoq4X-Nu2EAphEAiCQSlhaBFaYElJIqROCA4z7OxCjxutSjeQ1W",
        "couleur":  0xf59e0b,
        "requis":   ["2to","2tb","2 to","2 tb"],
        "blacklist": ["500go","500gb","512go","1to","1tb","sata","boitier","adaptateur","cable","support","portable","laptop"],
    },
    {
        "nom":      "RAM DDR4 8Go",
        "search":   "ram ddr4 8go",
        "prix_min": 0,
        "prix_max": 15,
        "webhook":  "https://discord.com/api/webhooks/1505674794006351872/sPkRfP_-K6OaKUj7hNJLdbnUY0zehmZ7W50Q99niPt9mkv3hJ-3AWdkKJygMsaxJisOf",
        "couleur":  0xec4899,
        "requis":   ["8go","8gb","8 go","8 gb"],
        "blacklist": ["16go","16gb","32go","32gb","64go","64gb","ddr3","ddr5","portable","laptop"],
    },
    {
        "nom":      "RAM DDR4 16Go",
        "search":   "ram ddr4 16go",
        "prix_min": 0,
        "prix_max": 20,
        "webhook":  "https://discord.com/api/webhooks/1505674794006351872/sPkRfP_-K6OaKUj7hNJLdbnUY0zehmZ7W50Q99niPt9mkv3hJ-3AWdkKJygMsaxJisOf",
        "couleur":  0xec4899,
        "requis":   ["16go","16gb","16 go","16 gb"],
        "blacklist": ["8go","8gb","32go","32gb","64go","64gb","ddr3","ddr5","portable","laptop"],
    },
    {
        "nom":      "RAM DDR4 32Go",
        "search":   "ram ddr4 32go",
        "prix_min": 0,
        "prix_max": 35,
        "webhook":  "https://discord.com/api/webhooks/1505674794006351872/sPkRfP_-K6OaKUj7hNJLdbnUY0zehmZ7W50Q99niPt9mkv3hJ-3AWdkKJygMsaxJisOf",
        "couleur":  0xec4899,
        "requis":   ["32go","32gb","32 go","32 gb"],
        "blacklist": ["8go","8gb","16go","16gb","64go","64gb","ddr3","ddr5","portable","laptop"],
    },
    {
        "nom":      "RAM DDR4 64Go",
        "search":   "ram ddr4 64go",
        "prix_min": 0,
        "prix_max": 60,
        "webhook":  "https://discord.com/api/webhooks/1505674794006351872/sPkRfP_-K6OaKUj7hNJLdbnUY0zehmZ7W50Q99niPt9mkv3hJ-3AWdkKJygMsaxJisOf",
        "couleur":  0xec4899,
        "requis":   ["64go","64gb","64 go","64 gb"],
        "blacklist": ["8go","8gb","16go","16gb","32go","32gb","ddr3","ddr5","portable","laptop"],
    },
]

INTERVALLE = 6
# ============================================================

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Referer": "https://www.vinted.fr/",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

def fetch(categorie):
    try:
        r = requests.get(
            "https://www.vinted.fr/api/v2/catalog/items",
            headers=get_headers(),
            params={
                "search_text":   categorie["search"],
                "price_from":    categorie["prix_min"],
                "price_to":      categorie["prix_max"],
                "order":         "newest_first",
                "per_page":      20,
                "catalog_ids[]": categorie.get("catalog_ids", ""),
            },
            timeout=10,
        )
        if r.status_code == 401:
            print(f"  [{categorie['nom']}] Token expire - recuperes-en un nouveau")
            return []
        r.raise_for_status()
        items = r.json().get("items", [])

        requis    = categorie.get("requis", [])
        blacklist = categorie.get("blacklist", [])
        if requis or blacklist:
            filtered = []
            for item in items:
                titre = item.get("title", "").lower()
                if blacklist and any(b.lower() in titre for b in blacklist):
                    continue
                if requis and not any(r2.lower() in titre for r2 in requis):
                    continue
                filtered.append(item)
            return filtered
        return items
    except Exception as e:
        print(f"  [{categorie['nom']}] Erreur : {e}")
        return []

def envoyer_discord(item, categorie):
    titre   = item.get("title", "Annonce inconnue")
    prix    = item.get("price", {}).get("amount", "?")
    url     = f"https://www.vinted.fr/items/{item['id']}"
    ville   = item.get("city", "?") or "?"
    etat    = item.get("status", "?") or "?"
    vendeur = item.get("user", {}).get("login", "?")
    photos  = item.get("photos", [])
    photo   = photos[0].get("url") if photos else None

    embed = {
        "title":       titre,
        "url":         url,
        "color":       categorie["couleur"],
        "description": f"**{prix} EUR** — {etat}",
        "fields": [
            {"name": "Ville",   "value": ville,         "inline": True},
            {"name": "Vendeur", "value": f"@{vendeur}", "inline": True},
        ],
        "footer":    {"text": f"Vinted Monitor · {categorie['nom']} · {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"},
        "thumbnail": {"url": photo} if photo else {},
    }

    content = f"{titre} — {prix} EUR\n{url}"

    try:
        r = requests.post(
            categorie["webhook"],
            json={"content": content, "embeds": [embed]},
            timeout=10,
        )
        if r.status_code == 204:
            print(f"  [{categorie['nom']}] OK : {titre} — {prix}EUR")
        else:
            print(f"  [{categorie['nom']}] Erreur Discord {r.status_code}")
    except Exception as e:
        print(f"  [{categorie['nom']}] Erreur Discord : {e}")

def surveiller(categorie):
    seen = set()
    print(f"  {categorie['nom']} - chargement initial...")
    for i in fetch(categorie):
        seen.add(str(i["id"]))
    print(f"  {categorie['nom']} - {len(seen)} annonces ignorees, surveillance active")

    while True:
        time.sleep(INTERVALLE)
        items = fetch(categorie)
        nouvelles = [i for i in items if str(i["id"]) not in seen]
        for item in nouvelles:
            seen.add(str(item["id"]))
            envoyer_discord(item, categorie)
        if not nouvelles:
            print(f"  [{datetime.now().strftime('%H:%M:%S')}] {categorie['nom']} - rien de nouveau")

# Lancement
print("=" * 55)
print("  Vinted Multi-Bot -> Discord")
print(f"  {len(CATEGORIES)} categories · refresh {INTERVALLE}s")
print("=" * 55)
for c in CATEGORIES:
    print(f"  {c['nom']} | {c['prix_min']}EUR-{c['prix_max']}EUR")
print("=" * 55 + "\n")

threads = []
for cat in CATEGORIES:
    t = threading.Thread(target=surveiller, args=(cat,), daemon=True)
    t.start()
    threads.append(t)
    time.sleep(1)

for t in threads:
    t.join()
