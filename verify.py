#!/usr/bin/env python3
"""Re-check the 1517 claim against the live Google Groups pages.

Asserts the two postings carry the expected in-document date headers, that the
Dec 1993 one contains the ".GIF" answer, and that the Oct 1993 one does not.
"""
import html
import re
import sys
import urllib.request

DEC93 = "https://groups.google.com/g/soc.singles/c/qye9q0j0vOE/m/Mrr5Rblz9OAJ"
OCT93 = "https://groups.google.com/g/soc.singles/c/9FyVS_dTm2k/m/R7jQxgth6owJ"

HEADERS = {"user-agent": "Mozilla/5.0 (compatible; poidh-1517-verify/1.0)"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode("utf-8", "ignore")
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", html.unescape(text))
    dates = re.findall(r"([A-Z][a-z]{2} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s?[AP]M)", text)
    return text, sorted(set(dates))


def main():
    ok = True

    text, dates = fetch(DEC93)
    has_hdr = "Last-modified: 1993/12/08" in text
    has_gif = "jokingly ask for a" in text
    print(f"DEC 1993  post dates={dates}")
    print(f"          Last-modified: 1993/12/08 -> {has_hdr}")
    print(f"          '.GIF' answer present       -> {has_gif}")
    ok &= has_hdr and has_gif

    text2, dates2 = fetch(OCT93)
    has_hdr2 = "Last-modified: 1993/09/06" in text2
    no_gif = "jokingly ask for a" not in text2 and "Graphics Interchange" not in text2
    print(f"OCT 1993  post dates={dates2}")
    print(f"          Last-modified: 1993/09/06 -> {has_hdr2}")
    print(f"          '.GIF' answer absent        -> {no_gif}")
    ok &= has_hdr2 and no_gif

    print("\nRESULT:", "PASS — the Dec 1993 FAQ documents the rule; the Oct 1993 one does not."
          if ok else "FAIL — one of the assertions did not hold; sources may have moved.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
