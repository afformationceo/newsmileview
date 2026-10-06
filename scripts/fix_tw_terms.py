"""대만어 페이지: 의미 오역·임상 오역 교정 + 메뉴 라벨 통일 (용어 감사 결과 중 우선순위 high)."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent

NAV = {
    "about": "診所介紹",
    "invisalign": "隱適美",
    "orthodontics": "牙齒矯正",
    "teeth-whitening": "牙齒美白",
    "laminate-veneers": "單日陶瓷貼片",
    "sleep-implant": "舒眠植牙",
    "prosthetics": "全瓷冠・假牙",
}
H1 = {
    "laminate-veneers": "單日陶瓷貼片",
    "sleep-implant": "舒眠植牙",
    "prosthetics": "全瓷冠・假牙修復",
}
BODY = [
    # 術前矯正 = '수술 전 교정'으로 의미가 반대 → 수술 우선 교정
    ("術前矯正", "手術優先矯正"),
    ("Surgery First術前優先", "Surgery First 手術優先"),
    # 워킹 블리칭은 실활치(신경 죽은 치아) 대상 → 활수(活髓)는 임상 오역
    ("活髓漂白", "內漂白（死髓牙美白）"),
    ("睡眠植牙", "舒眠植牙"),
    ("麻醉疼痛醫學科專科醫師", "麻醉專科醫師"),
    # 대만 健保로 오인 방지 (외국인 관광객은 한국 건강보험 비대상)
    ("等可納入健保給付的治療方式", "等治療方式"),
    ("可申請健保給付", "預防並改善牙周病"),
    ("洗牙、樹脂填補等預防並改善牙周病", "洗牙、樹脂填補等基礎治療"),
    ("健保每年給付1次洗牙，", ""),
]
n = 0
for f in sorted((ROOT / "zh-tw").glob("*.html")):
    s = o = f.read_text(encoding="utf-8")
    for a, b in BODY:
        s = s.replace(a, b)
    for slug, label in NAV.items():
        s = re.sub(rf'(<a href="/zh-tw/{slug}"(?: class="active")?>)[^<]+(</a>)', rf"\g<1>{label}\2", s)
    if f.stem in H1:
        s = re.sub(r'(<h1 class="lm-kr-sub">)[^<]*(</h1>)', rf"\g<1>{H1[f.stem]}\2", s, count=1)
    if s != o:
        f.write_text(s, encoding="utf-8"); n += 1
print("zh-tw files updated:", n)
