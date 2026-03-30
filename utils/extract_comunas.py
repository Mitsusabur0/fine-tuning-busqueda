import csv
from html.parser import HTMLParser
from pathlib import Path


input_path = "raw.html"
output_path = "lista_comunas.csv"


class SpanTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_span = False
        self._current_text: list[str] = []
        self.texts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "span":
            self._inside_span = True
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._inside_span:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "span" and self._inside_span:
            text = "".join(self._current_text).strip()
            if text:
                self.texts.append(text)
            self._inside_span = False
            self._current_text = []


def parse_comuna_entry(entry: str) -> tuple[str, str] | None:
    if "," not in entry:
        return None

    comuna, region = entry.split(",", 1)
    comuna = comuna.strip()
    region = region.strip()

    if region.startswith("(") and region.endswith(")"):
        region = region[1:-1].strip()

    if not comuna or not region:
        return None

    return comuna, region


def main() -> None:
    html_content = Path(input_path).read_text(encoding="utf-8")

    parser = SpanTextExtractor()
    parser.feed(html_content)

    rows = []
    for entry in parser.texts:
        parsed = parse_comuna_entry(entry)
        if parsed is not None:
            rows.append(parsed)

    with Path(output_path).open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["comuna", "region"])
        writer.writerows(rows)

    print(f"Extracted {len(rows)} comunas to {output_path}")


if __name__ == "__main__":
    main()
