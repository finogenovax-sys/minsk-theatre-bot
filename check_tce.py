
import urllib.request
import urllib.error

url = "https://tce.by/"

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "MinskTheatreBot/0.1 (availability research)"
    }
)

try:
    with urllib.request.urlopen(request, timeout=15) as response:
        print("HTTP status:", response.status)
        print("Final URL:", response.geturl())
        print("Content type:", response.headers.get("Content-Type"))
        print("Access test completed")

except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)
    print("Server refused or restricted the request")

except urllib.error.URLError as error:
    print("Connection error:", error.reason)
