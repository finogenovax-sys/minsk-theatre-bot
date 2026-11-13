
import json
import urllib.request
import urllib.error
import http.client

BASE = "RkZDMTE2MUQtMTNFNy00NUIyLTg0QzYtMURDMjRBNTc1ODA0"
SHOW_ID = "5101"

url = (
    "https://tce.by/index.php"
    "?view=shows&action=ticket&kind=json"
    f"&base={BASE}&base={BASE}&data={SHOW_ID}"
)

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*",
        "Referer": (
            f"https://tce.by/shows.html?base={BASE}"
            f"&data={SHOW_ID}"
        ),
    },
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read().decode("utf-8", errors="replace")
        print("HTTP status:", response.status)

    result = json.loads(raw)

    print("API success:", result.get("success"))

    if result.get("success") is True:
        tickets = result.get("data")
        if isinstance(tickets, list):
            print("Available ticket records:", len(tickets))
            print("Sample:", tickets[:2])
        else:
            print("Unexpected ticket data:", type(tickets).__name__)
    else:
        print("API message:", result.get("data"))
        print("Availability not confirmed")

except (
    urllib.error.URLError,
    http.client.RemoteDisconnected,
    TimeoutError,
    ConnectionError,
    OSError,
    ValueError,
) as error:
    print("CHECK FAILED:", type(error).__name__)
    print("Details:", str(error))
    raise SystemExit(1)
