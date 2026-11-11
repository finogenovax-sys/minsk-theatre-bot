
import os
import re
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

URL = "https://puppet-minsk.by/afisha"
ADULT_URL = "https://puppet-minsk.by/spektakli/spektakli-dlya-vzroslykh"
STATE_FILE = Path("afisha_state.json")

DATE_RE = re.compile(
    r"^\d{2}\.\d{2}\.20\d{2}\s+\d{2}:\d{2}$"
)


class AfishaParser(HTMLParser):
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




class AdultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.titles = set()

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            classes = dict(attrs).get("class", "").split()
            if "spectacli-title" in classes:
                self.in_title = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.titles.add(" ".join(data.split()).casefold())


def get_adult_titles():
    request = urllib.request.Request(
        ADULT_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = AdultParser()
    parser.feed(html)

    if not parser.titles:
        raise RuntimeError("Adult performances not found")

    return parser.titles


def get_events():
    adult_titles = get_adult_titles()
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = AfishaParser()
    parser.feed(html)

    months = (
        "января|февраля|марта|апреля|мая|июня|"
        "июля|августа|сентября|октября|ноября|декабря"
    )
    date_pattern = re.compile(
        rf"^\d{{1,2}}\s+({months})\b",
        re.IGNORECASE
    )

    events = set()
    texts = parser.text
    print("ВСЕГО ЭЛЕМЕНТОВ:", len(texts))
    print("ПЕРВЫЕ 100 ЭЛЕМЕНТОВ:", repr(texts[:100]))

    for i, value in enumerate(texts):
        if not date_pattern.match(value):
            continue

        date = value
        title = ""

        for candidate in texts[i + 1:i + 7]:
            if date_pattern.match(candidate):
                break
            if candidate.lower() in ("купить билет", "билеты"):
                continue
            if re.fullmatch(r"\d{1,2}:\d{2}", candidate):
                continue
            if len(candidate) > 2:
                title = candidate
                break
            if title:
                print("АФИША:", repr(title))
                print("ЕСТЬ В СПИСКЕ ВЗРОСЛЫХ:",
                      title.casefold() in adult_titles)

            if title and title.casefold() in adult_titles:
                events.add(f"{date} | {title}")

    print("ВЗРОСЛЫЕ СПЕКТАКЛИ:", sorted(adult_titles))
    print("НАЙДЕНО СОБЫТИЙ:", len(events))
    return sorted(events)

def send_telegram(message):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode("utf-8")

    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        method="POST"
    )

    with urllib.request.urlopen(
        request, timeout=20
    ) as response:
        result = json.load(response)

    if not result.get("ok"):
        raise RuntimeError("Telegram error")


def main():
    current = get_events()

    if not current:
        raise RuntimeError(
            "No events found. State not updated."
        )

    print("Events found:", len(current))

    if not STATE_FILE.exists():
        STATE_FILE.write_text(
            json.dumps(
                current, ensure_ascii=False, indent=2
            ),
            encoding="utf-8"
        )
        print("Initial afisha saved")
        return

    previous = json.loads(
        STATE_FILE.read_text(encoding="utf-8")
    )

    new_events = sorted(
        set(current) - set(previous)
    )

    if new_events:
        message = (
            "🎭 АФИША ТЕАТРА КУКОЛ ОБНОВИЛАСЬ!\n\n"
            + "\n".join(
                "🎟 " + event
                for event in new_events[:20]
            )
            + "\n\n" + URL
        )

        send_telegram(message)
        print("Notification sent:", len(new_events))
    else:
        print("No new events")

    STATE_FILE.write_text(
        json.dumps(
            current, ensure_ascii=False, indent=2
        ),
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
