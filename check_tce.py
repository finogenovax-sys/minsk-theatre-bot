
import urllib.request
import urllib.error
import http.client

url = (
    "https://tce.by/shows.html"
    "?base=RkZDMTE2MUQtMTNFNy00NUIyLTg0QzYtMURDMjRBNTc1ODA0"
    "&data=5265"
)

request = urllib.request.Request(
    url,
    headers={"User-Agent": "MinskTheatreBot/0.1"}
)

try:
    with urllib.request.urlopen(request, timeout=15) as response:
        print("HTTP status:", response.status)
        print("Content type:", response.headers.get("Content-Type"))
        print("Page received:", len(response.read()), "bytes")

except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)

except (
    urllib.error.URLError,
    http.client.RemoteDisconnected,
    TimeoutError,
    ConnectionError
) as error:
    print("Connection failed:", type(error).__name__)
    print("Details:", str(error))
