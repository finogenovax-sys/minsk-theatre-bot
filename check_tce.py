
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/157.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://tce.by/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

import urllib.request
import urllib.error
import http.client
import json

BASE = "RkZDMTE2MUQtMTNFNy00NUIyLTg0QzYtMURDMjRBNTc1ODA0"
SHOW_ID = "5101"

tests = [
    (
        "1. Главная страница",
        "https://tce.by/"
    ),
    (
        "2. Страница спектакля",
        f"https://tce.by/shows.html?base={BASE}&data={SHOW_ID}"
    ),
    (
        "3. API билетов (один base)",
        f"https://tce.by/index.php?view=shows&action=ticket&kind=json&base={BASE}&data={SHOW_ID}"
    ),
    (
        "4. API билетов (два base)",
        f"https://tce.by/index.php?view=shows&action=ticket&kind=json&base={BASE}&base={BASE}&data={SHOW_ID}"
    )
]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*",
    "Referer": (
        f"https://tce.by/shows.html?base={BASE}&data={SHOW_ID}"
    ),
    "Connection": "close"
}

for name, url in tests:
    print("\n" + "=" * 50)
    print(name)

    request = urllib.request.Request(
        url,
        headers=headers
    )

    try:
        with urllib.request.urlopen(
            request, timeout=20
        ) as response:
            body = response.read()

            print("STATUS:", response.status)
            print("CONTENT TYPE:", response.headers.get("Content-Type"))
            print("SIZE:", len(body), "bytes")

            decoded = body.decode(
                "utf-8", errors="replace"
            )

            try:
                data = json.loads(decoded)
                print("JSON:", json.dumps(
                    data, ensure_ascii=False
                )[:700])
            except ValueError:
                print("RESPONSE:", decoded[:500])

    except urllib.error.HTTPError as error:
        print("HTTP ERROR:", error.code)
        print("DETAILS:", error.read(500).decode(
            "utf-8", errors="replace"
        ))

    except Exception as error:
        print("CONNECTION ERROR:", type(error).__name__)
        print("DETAILS:", str(error))

print("\nDIAGNOSTICS COMPLETED")
