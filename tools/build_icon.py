from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "app_icon.ico"


def build() -> None:
    size = 512
    image = Image.new("RGBA", (size, size), (4, 15, 28, 255))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, 492, 492), radius=110, fill=(7, 28, 51, 255), outline=(29, 168, 255, 255), width=10)
    bubble = [(112, 135), (400, 135), (454, 189), (454, 321), (400, 375), (245, 375), (163, 440), (163, 375), (112, 375), (58, 321), (58, 189)]
    draw.polygon(bubble, fill=(8, 26, 46, 255))
    draw.line(bubble + [bubble[0]], fill=(35, 216, 255, 255), width=14, joint="curve")
    draw.line((151, 230, 205, 272, 151, 314), fill=(35, 220, 255, 255), width=18, joint="curve")
    draw.line((230, 320, 352, 320), fill=(109, 133, 255, 255), width=18)
    draw.ellipse((320, 202, 356, 238), fill=(35, 220, 255, 255))
    draw.ellipse((372, 202, 408, 238), fill=(109, 133, 255, 255))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(OUT)


if __name__ == "__main__":
    build()
