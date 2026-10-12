"""페이지에서 참조하는 큰 PNG/JPG → WebP 변환 + HTML 참조 교체. 재실행 안전.

원본은 그대로 두고 같은 폴더에 .webp를 만든다(가로 최대 1600px).
WebP가 원본보다 작을 때만 참조를 바꾼다. OG 이미지(절대 URL)는 대상 아님.
GIF → MP4 변환은 ffmpeg로 따로 했다 (images/invisalign/step_0N.mp4).
"""
import re
import urllib.parse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MIN_BYTES = 100_000
MAX_W = 1600
REF = re.compile(r"""(?<=["'(])(/?images/[^"')]+?)\.(png|jpe?g)(?=["')])""", re.I)


def pages():
    for d in ("", "ja", "zh-tw"):
        for p in sorted((ROOT / d).glob("*.html")):
            if not p.name.startswith("source_"):
                yield p


def to_webp(src: Path) -> Path | None:
    dst = src.with_suffix(".webp")
    if not dst.exists():
        im = Image.open(src)
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() or "transparency" in im.info else "RGB")
        im.save(dst, "WEBP", quality=80, method=6)
    return dst if dst.stat().st_size < src.stat().st_size else None


def main():
    cache, before, after = {}, 0, 0
    for page in pages():
        s = page.read_text(encoding="utf-8")

        def repl(m):
            nonlocal before, after
            raw = m.group(1)
            src = ROOT / urllib.parse.unquote(raw.lstrip("/") + "." + m.group(2))
            if not src.exists() or src.stat().st_size < MIN_BYTES:
                return m.group(0)
            if src not in cache:
                cache[src] = to_webp(src)
                if cache[src]:
                    before += src.stat().st_size
                    after += cache[src].stat().st_size
            return raw + ".webp" if cache[src] else m.group(0)

        n = REF.sub(repl, s)
        if n != s:
            page.write_text(n, encoding="utf-8")
            print("updated", page.relative_to(ROOT))
    print(f"{len([v for v in cache.values() if v])} images: "
          f"{before / 1e6:.1f}MB → {after / 1e6:.1f}MB")


if __name__ == "__main__":
    main()
