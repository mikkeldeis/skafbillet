import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
import webbrowser
from config import URL


def tjek_billet():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        billet_links = soup.find_all("a", class_="btn btn-primary")

        for link in billet_links:
            href = link.get("href", "")
            if "/event/261/resale/ticket/" in href:
                link_url = f"https://www.aarhusmotion.dk{href}"
                print("🎉 Der er en billet til salg!")
                print("👉", link_url)

                # Send systemnotifikation
                notification.notify(
                    title="🎟️ Billet fundet!",
                    message="Åbner siden i din browser...",
                    timeout=10
                )
                # Åbn linket i din standardbrowser
                webbrowser.open(link_url)
                return True
        print("Ingen billetter lige nu.")
    except Exception as e:
        print("Fejl ved hentning af siden:", e)

    return False

# Kør hvert 5. minut
while True:
    print("Tjekker for billetter...")
    fundet = tjek_billet()
    if fundet:
        break  # Stop når billet er fundet
    time.sleep(300)
