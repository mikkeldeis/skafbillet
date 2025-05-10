import time
import requests
from bs4 import BeautifulSoup
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    print("Advarsel: plyer eller pyobjus ikke tilgængelig, systemnotifikationer virker ikke.")
    PLYER_AVAILABLE = False
import webbrowser
from config import URL


def tjek_billet():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)
        if response.status_code != 200:
            print("Fejl ved hentning af siden:", response.status_code)
            return False
        print(f"response code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        billet_links = soup.find_all("a", class_="btn btn-primary")
        for link in billet_links:
            # Tjek om linket indeholder "/event/261/resale/ticket/"
            print("tjekker link:", link)
            if "/event/261/resale/ticket/" in link.get("href"):
                href = link.get("href")
                print("Billet fundet:", href)
                # Åbn linket i din standardbrowser
                link_url = "https://www.aarhusmotion.dk/" + href
                response = requests.get(link_url, headers=headers)
                if response.status_code != 200:
                    print("Fejl ved hentning af billetlink:", response.status_code)
                    return False
                # Check for alert indicating tickets are sold or reserved
                alert = BeautifulSoup(response.text, 'html.parser').find(
                    "div", class_="alert alert-danger"
                )
                if alert and "not possible to select this at the moment" in alert.text:
                    print("Billet ikke tilgængelig, prøver igen...")
                    return False
                webbrowser.open(link_url)
                return True
        print("Ingen billetter lige nu.")
    except Exception as e:
        print("Fejl ve  d hentning af siden:", e)

    return False

while True:
    print("Tjekker for billetter...")
    fundet = tjek_billet()
    if fundet:
        break  # Stop når billet er fundet
    time.sleep(300)
