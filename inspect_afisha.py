
import re
import urllib.request
from html.parser import HTMLParser

URL = "https://puppet-minsk.by/afisha"

class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            value = " ".join(data.split())
            if value:
                self.text.append(value)

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "MinskTheatreBot/0.1"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8", errors="replace")

parser = PageInspector()
parser.feed(html)

print("HTML size:", len(html))
print("Visible text fragments:", len(parser.text))

print("\nFIRST 100 TEXT FRAGMENTS:")
for line in parser.text[:100]:
    print(line[:180])

print("\nDATE PATTERNS:")
patterns = [
    r"\b\d{1,2}\.\d{1,2}\.20\d{2}\b",
    r"\b20\d{2}-\d{2}-\d{2}\b",
]

for pattern in patterns:
    matches = re.findall(pattern, html)
    print(pattern, ":", len(matches))
    print("Examples:", matches[:10])
