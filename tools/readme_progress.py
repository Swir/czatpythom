from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
STATUS = ROOT / "STATUS.md"
ASSETS = ROOT / "assets" / "readme"
CARD = ASSETS / "progress-card.svg"
MINI = ASSETS / "progress-mini.svg"
TEMPLATE = ASSETS / "progress-template.svg"

PROJECT = "CzatPythom"
SCOPE = "Product completion · no canonical measurable roadmap"
STATE = "PUBLISHED v2.1.0"
COUNTER = "No trustworthy product denominator; latest public release v2.1.0."

LEGACY_PATTERNS = (
    re.compile(r"[█▓▒░]{6,}"),
    re.compile(r"\[[#=\-]{6,}\]"),
)


def card_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc">
<title id="title">{PROJECT} progress</title><desc id="desc">{PROJECT}. Scope: {SCOPE}. Status: {STATE}. Progress: N/A. No trustworthy product denominator.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#62E5FF" stroke-opacity="0.045"/></pattern></defs>
<rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#bg)" stroke="#62E5FF" stroke-opacity="0.25"/><rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#grid)"/><text x="50" y="34" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700" letter-spacing="3">SWIR PROGRESS</text><text x="50" y="67" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="800">{PROJECT}</text><text x="50" y="92" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="14">{SCOPE}</text><text x="1150" y="67" text-anchor="end" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="34" font-weight="800">N/A</text><text x="1150" y="92" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">{STATE}</text><rect x="50" y="111" width="1100" height="18" rx="9" fill="#08131F" stroke="#62E5FF" stroke-opacity="0.15"/><text x="50" y="154" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="13">{COUNTER}</text><text x="1150" y="154" text-anchor="end" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="13">Source: STATUS.md</text></svg>'''


def mini_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="72" viewBox="0 0 900 72" role="img" aria-labelledby="title desc"><title id="title">{PROJECT} compact progress</title><desc id="desc">{SCOPE}. N/A. Latest public release v2.1.0.</desc><rect x="1" y="1" width="898" height="70" rx="18" fill="#02050A" stroke="#62E5FF" stroke-opacity="0.25"/><text x="22" y="28" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">{PROJECT}</text><text x="22" y="50" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="11">N/A · {STATE}</text><rect x="170" y="27" width="700" height="16" rx="8" fill="#07111C" stroke="#62E5FF" stroke-opacity="0.15"/><text x="870" y="58" text-anchor="end" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="10">No canonical product denominator</text></svg>'''


def template_svg() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc"><title id="title">SWIR progress template</title><desc id="desc">TEMPLATE / NOT PROJECT DATA. Reusable visual shell for deterministic project progress generation.</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient></defs><rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#bg)" stroke="#62E5FF" stroke-opacity="0.25"/><text x="50" y="42" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="700">TEMPLATE / NOT PROJECT DATA</text><text x="50" y="82" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="800">PROJECT NAME · SCOPE</text><rect x="50" y="111" width="1100" height="18" rx="9" fill="#07111C" stroke="#62E5FF" stroke-opacity="0.18"/><text x="50" y="154" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="13">Generate from one authoritative source. Do not embed this template as live progress.</text></svg>'''


def expected() -> dict[Path, str]:
    return {CARD: card_svg(), MINI: mini_svg(), TEMPLATE: template_svg()}


def validate_svg(text: str) -> None:
    root = ET.fromstring(text)
    viewbox = root.attrib.get("viewBox", "")
    if len(viewbox.split()) != 4:
        raise SystemExit("invalid viewBox")
    if "XXX" in text or "NaN" in text or "Infinity" in text:
        raise SystemExit("invalid SVG placeholder/number")


def check_legacy_meters() -> None:
    for path in (README, STATUS):
        text = path.read_text(encoding="utf-8")
        for pattern in LEGACY_PATTERNS:
            if pattern.search(text):
                raise SystemExit(f"legacy progress meter detected in {path.relative_to(ROOT)}")


def write() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for path, text in expected().items():
        validate_svg(text)
        path.write_text(text, encoding="utf-8")


def check() -> None:
    check_legacy_meters()
    for path, text in expected().items():
        validate_svg(text)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            raise SystemExit(f"stale generated asset: {path.relative_to(ROOT)}")
    if "assets/readme/progress-card.svg" not in README.read_text(encoding="utf-8"):
        raise SystemExit("README progress card is not embedded")
    if "assets/readme/progress-mini.svg" not in STATUS.read_text(encoding="utf-8"):
        raise SystemExit("STATUS progress mini is not embedded")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
        print("README progress check: OK")
    else:
        write()
        check()
        print("README progress assets regenerated and verified")


if __name__ == "__main__":
    main()
