"""진료시간을 CS 시스템(챗닥) 승인 정보 기준으로 전 페이지 통일.

월·화·수·금 10:00~18:30 (점심 13:00~14:00), 토 10:00~15:00, 목·일·공휴일 휴진.
재실행 안전: hours-table / footer-hours 블록을 통째로 교체한다.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

T = {
    "": dict(
        weekdays="월 | 화 | 수 | 금", sat="토요일", lunch="점심시간",
        holiday="목요일, 일요일, 공휴일은 휴진입니다.",
        f_weekdays="월·화·수·금", f_lunch="점심시간 PM 01:00 - PM 02:00",
        f_sat="토요일", f_sat_note="점심시간 없이 진료",
        f_closed="휴진", f_closed_days="목·일·공휴일",
    ),
    "ja": dict(
        weekdays="月 | 火 | 水 | 金", sat="土曜日", lunch="昼休み",
        holiday="木曜日・日曜日・祝日は休診です。",
        f_weekdays="月・火・水・金", f_lunch="昼休み PM 01:00 - PM 02:00",
        f_sat="土曜日", f_sat_note="昼休みなし診療",
        f_closed="休診", f_closed_days="木・日・祝日",
    ),
    "zh-tw": dict(
        weekdays="週一 | 週二 | 週三 | 週五", sat="週六", lunch="午休時間",
        holiday="週四、週日及國定假日休診。",
        f_weekdays="週一·二·三·五", f_lunch="午休時間 PM 01:00 - PM 02:00",
        f_sat="週六", f_sat_note="無午休持續看診",
        f_closed="休診", f_closed_days="週四·週日·國定假日",
    ),
}


def hours_table(t, ind):
    rows = [(t["weekdays"], "am 10:00 - pm 06:30"),
            (t["sat"], "am 10:00 - pm 03:00"),
            (t["lunch"], "pm 01:00 - pm 02:00")]
    out = [f'{ind}<div class="hours-table">']
    for label, time in rows:
        out += [f'{ind}    <div class="h-row">',
                f'{ind}        <span class="h-label">{label}</span>',
                f'{ind}        <span class="h-time">{time}</span>',
                f'{ind}    </div>']
    out += [f'{ind}</div>', f'{ind}<p class="holiday-notice">{t["holiday"]}</p>']
    return "\n".join(out)


def footer_hours(t, ind):
    return "\n".join([
        f'{ind}<ul class="footer-hours">',
        f'{ind}    <li><span class="day">{t["f_weekdays"]}</span><span>AM 10:00 - PM 06:30</span></li>',
        f'{ind}    <li class="note">{t["f_lunch"]}</li>',
        f'{ind}    <li><span class="day">{t["f_sat"]}</span><span>AM 10:00 - PM 03:00</span></li>',
        f'{ind}    <li class="note">{t["f_sat_note"]}</li>',
        f'{ind}    <li class="closed"><span class="day">{t["f_closed"]}</span><span>{t["f_closed_days"]}</span></li>',
        f'{ind}</ul>',
    ])


def sv_hours_table(t, ind):
    """about 페이지 본문 HOURS 블록."""
    def row(day, time, cls="sv-hours-row"):
        return [f'{ind}    <div class="{cls}">',
                f'{ind}        <span class="sv-hours-day">{day}</span>',
                f'{ind}        <span class="sv-hours-time">{time}</span>',
                f'{ind}    </div>']
    return "\n".join(
        [f'{ind}<div class="sv-hours-table">']
        + row(t["f_weekdays"], "AM 10:00 - PM 06:30")
        + [f'{ind}    <div class="sv-hours-note">{t["f_lunch"]}</div>']
        + row(t["f_sat"], "AM 10:00 - PM 03:00")
        + [f'{ind}    <div class="sv-hours-note">{t["f_sat_note"]}</div>']
        + row(t["f_closed"], t["f_closed_days"], "sv-hours-row sv-hours-closed")
        + [f'{ind}</div>'])


SV_RE = re.compile(r'^([ \t]*)<div class="sv-hours-table">.*?sv-hours-closed">.*?</div>\n[ \t]*</div>', re.S | re.M)
TABLE_RE = re.compile(r'^([ \t]*)<div class="hours-table">.*?<p class="holiday-notice">.*?</p>', re.S | re.M)
FOOTER_RE = re.compile(r'^([ \t]*)<ul class="footer-hours">.*?</ul>', re.S | re.M)


def main():
    for lang, t in T.items():
        for path in sorted((ROOT / lang).glob("*.html")):
            if path.name.startswith("source_"):
                continue
            s = path.read_text(encoding="utf-8")
            n = s
            n = TABLE_RE.sub(lambda m: hours_table(t, m.group(1)), n)
            n = SV_RE.sub(lambda m: sv_hours_table(t, m.group(1)), n)
            n = FOOTER_RE.sub(lambda m: footer_hours(t, m.group(1)), n)
            if n != s:
                path.write_text(n, encoding="utf-8")
                print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
