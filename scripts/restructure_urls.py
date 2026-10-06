"""1회성: 평면 구조(implant_jp.html) → 언어 폴더 + SEO 슬러그(/ja/sleep-implant) 전환.

- 파일 이동(git mv), 내부 링크/언어 선택기/자산 경로(절대경로화) 재작성
- 예전 URL → 새 URL 301 리디렉트를 vercel.json에 생성
"""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

SLUG = {
    "index": "",
    "introduction": "about",
    "implant": "sleep-implant",
    "invisalign": "invisalign",
    "laminate": "laminate-veneers",
    "ortho": "orthodontics",
    "prosthetics": "prosthetics",
    "whitening": "teeth-whitening",
}
LANG_DIR = {"": "", "_jp": "ja", "_tw": "zh-tw"}
LEGACY = ["brand", "staff", "location_guide", "treatment"]  # KO 전용, 위치 유지


def new_url(base, sfx):
    parts = [p for p in (LANG_DIR[sfx], SLUG[base]) if p]
    return "/" + "/".join(parts)


def new_file(base, sfx):
    d, s = LANG_DIR[sfx], SLUG[base]
    return pathlib.Path(d) / f"{s or 'index'}.html"


def old_url(base, sfx):
    name = f"{base}{sfx}"
    return "/" if name == "index" else f"/{name}"


URL_MAP = {old_url(b, s): new_url(b, s) for b in SLUG for s in LANG_DIR}


def rewrite(text, sfx):
    # 내부 페이지 링크 (쿼리/해시 유지)
    def link(m):
        path, rest = m.group(1), m.group(2) or ""
        return f'href="{URL_MAP.get(path, path)}{rest}"'
    text = re.sub(r'href="(/[A-Za-z0-9_]*)([?#][^"]*)?"', link, text)
    # 자산 경로 절대화: 하위 폴더 페이지에서도 동일하게 동작
    text = re.sub(r'''(["'`(])(images|css|js)/''', r"\1/\2/", text)
    return text


def fix_ko_switcher(text, base):
    """JP/TW 페이지의 한국어 링크: 404 외부 사이트 → 같은 내용의 KO 페이지."""
    return re.sub(r'<a href="https://www\.smile-vdental\.com/home" target="_blank">',
                  f'<a href="{new_url(base, "")}">', text)


def main():
    pages = []
    for b in SLUG:
        for s in LANG_DIR:
            src, dst = pathlib.Path(f"{b}{s}.html"), new_file(b, s)
            (ROOT / dst).parent.mkdir(parents=True, exist_ok=True)
            if src != dst:
                subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)
            pages.append((dst, b, s))
    pages += [(pathlib.Path(f"{n}.html"), None, "") for n in LEGACY]

    for path, base, sfx in pages:
        f = ROOT / path
        t = rewrite(f.read_text(encoding="utf-8"), sfx)
        if base and sfx:
            t = fix_ko_switcher(t, base)
        f.write_text(t, encoding="utf-8")

    js = ROOT / "js/main.js"
    js.write_text(re.sub(r'''(["'`(])(images|css|js)/''', r"\1/\2/",
                         js.read_text(encoding="utf-8")), encoding="utf-8")

    redirects = []
    for old, new in URL_MAP.items():
        if old == "/":
            continue
        if old != new:
            redirects.append({"source": old, "destination": new, "permanent": True})
        redirects.append({"source": f"{old}.html", "destination": new, "permanent": True})
    cfg_path = ROOT / "vercel.json"
    cfg = json.loads(cfg_path.read_text())
    cfg["redirects"] = redirects
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"moved {len(pages) - len(LEGACY)} pages, {len(redirects)} redirects")


if __name__ == "__main__":
    main()
