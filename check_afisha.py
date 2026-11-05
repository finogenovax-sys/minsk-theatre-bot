
import urllib.request
import urllib.error
import http.client

url = "https://puppet-minsk.by/bilety/afisha"

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "MinskTheatreBot/0.1"
    }
)

try:
    with urllib.request.urlopen(request, timeout=15) as response:
        content = response.read()
        print("HTTP status:", response.status)
        print("Content type:", response.headers.get("Content-Type"))
        print("Page size:", len(content), "bytes")
        print("Afisha access: OK")

except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)
    print("Afisha access: FAILED")

except (
    urllib.error.URLError,
    http.client.RemoteDisconnected,
    TimeoutError,
    ConnectionError
) as error:
    print("Connection failed:", type(error).__name__)
    print("Afisha access: FAILED")
