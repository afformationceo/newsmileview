"""페이지별 SEO 메타(title/description/canonical/hreflang/OG/JSON-LD)를 <head>에 주입한다.

재실행해도 안전하다: <!-- SEO:START --> ~ <!-- SEO:END --> 블록을 통째로 교체한다.
사용: python3 scripts/seo_meta.py
"""
import json
import pathlib
import re

SITE = "https://www.smileview-dental.com"
OG_IMAGE = f"{SITE}/images/og/clinic.jpg"
ROOT = pathlib.Path(__file__).resolve().parent.parent

LANGS = {  # 언어 폴더 → (hreflang, og:locale)
    "": ("ko", "ko_KR"),
    "ja": ("ja", "ja_JP"),
    "zh-tw": ("zh-TW", "zh_TW"),
}
SITE_NAME = {
    "": "스마일뷰치과의원",
    "ja": "SMILEVIEWデンタルクリニック",
    "zh-tw": "SMILEVIEW牙醫診所",
}

# (title, description) — 시술명은 현지에서 실제 검색되는 표기 기준
META = {
    "index": {
        "": ("강남 치과 스마일뷰치과의원 | 인비절라인·라미네이트·수면 임플란트",
             "강남역 스마일뷰치과의원. 인비절라인 투명교정, 원데이 라미네이트, 수면 임플란트, 치아미백, 보철치료까지 정밀 진단과 편안한 진료로 자연스러운 미소를 디자인합니다."),
        "ja": ("韓国・江南の歯科 SMILEVIEWデンタルクリニック｜インビザライン・ラミネートベニア",
             "ソウル江南駅近くのSMILEVIEWデンタルクリニック。インビザライン、ワンデーラミネートベニア、静脈内鎮静法インプラント、ホワイトニング、セラミック治療まで。LINEでご相談・ご予約いただけます。"),
        "zh-tw": ("韓國江南牙醫 SMILEVIEW牙醫診所｜隱適美・陶瓷貼片・舒眠植牙",
             "首爾江南站附近的SMILEVIEW牙醫診所。提供隱適美隱形矯正、單日陶瓷貼片、舒眠植牙、牙齒美白與全瓷冠假牙，可透過LINE諮詢與預約。"),
    },
    "about": {
        "": ("병원소개 | 강남 스마일뷰치과의원",
             "강남역 1분 거리 스마일뷰치과의원을 소개합니다. 분야별 전문 의료진 협진, 디지털 진단 장비, 1:1 맞춤 상담으로 안전하고 정밀한 치과 진료를 제공합니다."),
        "ja": ("クリニック紹介｜韓国・江南の歯科 SMILEVIEW",
             "ソウル江南のSMILEVIEWデンタルクリニックをご紹介します。各分野の歯科医師による連携診療、デジタル診断設備、1対1のカウンセリングで、安全で精密な歯科治療を提供します。"),
        "zh-tw": ("診所介紹｜韓國江南牙醫 SMILEVIEW",
             "認識首爾江南的SMILEVIEW牙醫診所。各領域牙醫師協同診療、數位診斷設備與一對一諮詢，提供安全精準的牙科治療。"),
    },
    "sleep-implant": {
        "": ("강남 수면 임플란트 | 스마일뷰치과의원",
             "치과 공포증이 있어도 편안하게. 수면 마취 상태에서 3D 네비게이션으로 정밀하게 식립하는 스마일뷰 수면 임플란트. 발치 당일 식립, 뼈이식, 오스템 임플란트 사용."),
        "ja": ("韓国 インプラント（静脈内鎮静法）｜眠ったまま治療 SMILEVIEW",
             "歯科恐怖症や嘔吐反射が心配な方も、静脈内鎮静法で眠ったような状態のまま。3Dナビゲーションによる精密な埋入、抜歯即日インプラント、骨移植・サイナスリフトにも対応するソウル江南のSMILEVIEW。"),
        "zh-tw": ("韓國舒眠植牙（靜脈鎮靜）｜SMILEVIEW 江南",
             "怕痛、有牙科恐懼或嘔吐反射也能安心。在靜脈鎮靜下以3D導航精準植牙，支援拔牙當天植牙、補骨與上顎竇提升。首爾江南SMILEVIEW。"),
    },
    "invisalign": {
        "": ("강남 인비절라인 투명교정 | 스마일뷰치과의원",
             "눈에 띄지 않는 투명 교정장치 인비절라인. 3D 디지털 스캔과 치료 결과 사전 시뮬레이션, 인비절라인 인증의의 1:1 맞춤 설계로 편안하게 교정합니다."),
        "ja": ("韓国 インビザライン（マウスピース矯正）｜SMILEVIEW 江南",
             "目立たない透明なマウスピース矯正インビザライン。iTero 3DスキャンとClinCheckによる治療結果の事前シミュレーション、インビザライン認定医による1対1の治療計画。ソウル江南のSMILEVIEW。"),
        "zh-tw": ("韓國隱適美（Invisalign）隱形矯正｜SMILEVIEW 江南",
             "不顯眼的透明牙套隱適美。iTero 3D掃描與ClinCheck療程模擬，治療前即可預覽結果，由隱適美認證醫師一對一規劃。首爾江南SMILEVIEW。"),
    },
    "laminate-veneers": {
        "": ("강남 원데이 라미네이트 | 스마일뷰치과의원",
             "0.2mm 최소 삭제, IPS e.max 정품 사용. 디지털 스마일 디자인(DSD)과 원내 기공소로 하루 만에 완성하는 스마일뷰 원데이 라미네이트."),
        "ja": ("韓国 ラミネートベニア｜ワンデー・e.max｜SMILEVIEW 江南",
             "0.2mmの最小限の削合、IPS e.max正規品を使用。デジタルスマイルデザイン（DSD）と院内技工所で、1日で仕上げるワンデーラミネートベニア。ソウル江南のSMILEVIEW。"),
        "zh-tw": ("韓國陶瓷貼片｜單日完成 e.max全瓷貼片｜SMILEVIEW",
             "最少0.2mm微磨、使用IPS e.max正品。結合DSD數位微笑設計與院內技工所，一天完成的單日陶瓷貼片。首爾江南SMILEVIEW。"),
    },
    "orthodontics": {
        "": ("강남 치아교정·선수술 교정 | 스마일뷰치과의원",
             "주걱턱, 돌출입, 안면비대칭까지. 교정과 전문의 협진으로 진행하는 스마일뷰 치아교정과 선수술 교정(양악수술 연계)으로 빠른 심미 개선과 기능적 교합을 회복합니다."),
        "ja": ("韓国 歯列矯正・サージェリーファースト｜受け口・出っ歯｜SMILEVIEW",
             "受け口・出っ歯・顔面非対称の矯正に。両顎手術と連携したサージェリーファースト矯正で早期に見た目を改善し、機能的な噛み合わせを回復します。裏側矯正・部分矯正にも対応。"),
        "zh-tw": ("韓國牙齒矯正・手術優先正顎｜戽斗・暴牙｜SMILEVIEW",
             "戽斗、暴牙、顏面不對稱矯正。結合雙顎手術的手術優先（Surgery First）矯正，快速改善外觀並恢復咬合功能，也提供舌側矯正與局部矯正。"),
    },
    "prosthetics": {
        "": ("강남 보철치료 (크라운·브릿지) | 스마일뷰치과의원",
             "충치, 파절, 오래된 보철물 교체까지. 손상된 치아의 기능과 심미를 함께 회복하는 스마일뷰 보철치료(크라운·브릿지·인레이)."),
        "ja": ("韓国 セラミック治療・被せ物（補綴治療）｜SMILEVIEW 江南",
             "むし歯・破折・古い被せ物の交換まで。ジルコニア、ゴールド、メタルボンドから最適な素材を選び、歯の機能と見た目を回復するセラミック治療・補綴治療。"),
        "zh-tw": ("韓國全瓷冠・假牙修復｜SMILEVIEW 江南",
             "蛀牙、牙齒斷裂、舊假牙更換。從氧化鋯、金冠、金屬烤瓷牙中選擇最適合的材料，恢復牙齒功能與美觀的牙冠修復治療。"),
    },
    "teeth-whitening": {
        "": ("강남 치아미백 | 스마일뷰치과의원",
             "잇몸 보호 후 전문 미백제와 미백 광선으로 빠르고 안전하게. 변색·착색 고민을 해결하는 스마일뷰 전문가 치아미백. 시술 전후 비교 사례 확인."),
        "ja": ("韓国 ホワイトニング（オフィスホワイトニング）｜SMILEVIEW 江南",
             "歯ぐきを保護したうえで、専用薬剤と光照射で短時間に白い歯へ。変色・着色に悩む方のためのオフィスホワイトニング。施術前後の症例も掲載。ソウル江南のSMILEVIEW。"),
        "zh-tw": ("韓國牙齒美白（診間美白）｜SMILEVIEW 江南",
             "先保護牙齦，再以專業美白劑與光照，短時間讓牙齒變白。針對變色與色素沉澱的診間美白，附治療前後案例。首爾江南SMILEVIEW。"),
    },
}

# 메뉴에서 연결되지 않는 예전 템플릿 페이지(플레이스홀더 내용) → 검색 제외
NOINDEX = {
    "brand": ("브랜드 스토리 | 스마일뷰치과의원", ""),
    "staff": ("의료진 소개 | 스마일뷰치과의원", ""),
    "location_guide": ("오시는 길·진료시간 | 스마일뷰치과의원", ""),
    "treatment": ("진료안내 | 스마일뷰치과의원", ""),
}


def url(base, lang):
    parts = [p for p in (lang, "" if base == "index" else base) if p]
    return f"{SITE}/" + "/".join(parts)


def file_for(base, lang):
    return ROOT / lang / f"{base}.html"


def esc(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def block_for(base, sfx, title, desc):
    hl, locale = LANGS[sfx]
    lines = [
        "<!-- SEO:START -->",
        f'<meta name="description" content="{esc(desc)}">',
        f'<link rel="canonical" href="{url(base, sfx)}">',
    ]
    for s, (h, _) in LANGS.items():
        lines.append(f'<link rel="alternate" hreflang="{h}" href="{url(base, s)}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{url(base, "")}">')
    lines += [
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{esc(SITE_NAME[sfx])}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url(base, sfx)}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        f'<meta property="og:locale" content="{locale}">',
    ]
    lines += [f'<meta property="og:locale:alternate" content="{l}">'
              for s, (_, l) in LANGS.items() if s != sfx]
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    if base == "index":
        ld = {
            "@context": "https://schema.org",
            "@type": "Dentist",
            "name": SITE_NAME[sfx],
            "alternateName": ["SMILEVIEW Dental Clinic", "스마일뷰치과의원"],
            "url": url(base, sfx),
            "image": OG_IMAGE,
            "inLanguage": hl,
            "areaServed": "Seoul",
        }
        lines.append('<script type="application/ld+json">'
                     + json.dumps(ld, ensure_ascii=False) + "</script>")
    lines.append("<!-- SEO:END -->")
    return "\n    ".join(lines)


def apply(path, title, block):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", s, count=1, flags=re.S)
    s = re.sub(r"\s*<!-- SEO:START -->.*?<!-- SEO:END -->", "", s, flags=re.S)
    s = re.sub(r"(</title>)", r"\1\n    " + block.replace("\\", "\\\\"), s, count=1)
    path.write_text(s, encoding="utf-8")


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for base in META:
        for sfx in LANGS:
            out.append("  <url>")
            out.append(f"    <loc>{url(base, sfx)}</loc>")
            for s, (h, _) in LANGS.items():
                out.append(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{url(base, s)}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url(base, "")}"/>')
            out.append("  </url>")
    out.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    missing = [f"{b}{s}" for b, v in META.items() for s, m in v.items() if not m]
    if missing:
        raise SystemExit(f"메타 미작성: {missing}")
    for base, per in META.items():
        for sfx, (title, desc) in per.items():
            apply(file_for(base, sfx), title, block_for(base, sfx, title, desc))
    for base, (title, _) in NOINDEX.items():
        apply(ROOT / f"{base}.html", title,
              '<!-- SEO:START -->\n    <meta name="robots" content="noindex, follow">\n    <!-- SEO:END -->')
    sitemap()
    print(f"ok: {sum(len(v) for v in META.values())} pages + {len(NOINDEX)} noindex")


if __name__ == "__main__":
    main()
