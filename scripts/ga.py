"""GA4 태그 + 전환 이벤트(LINE/전화 클릭)를 모든 페이지 <head> 맨 앞에 주입. 재실행 안전."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
GA_ID = "G-FZ5TDWRL0T"

SNIPPET = f"""<!-- GA:START -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}');
      // 전환 측정: LINE 예약 / 전화 클릭 (GA4 > 관리 > 주요 이벤트에서 line_click, phone_click 지정)
      document.addEventListener('click', function (e) {{
        var a = e.target.closest && e.target.closest('a[href]');
        if (!a) return;
        var href = a.getAttribute('href');
        var name = /^https:\\/\\/lin\\.ee\\//.test(href) ? 'line_click' : /^tel:/.test(href) ? 'phone_click' : null;
        if (!name) return;
        gtag('event', name, {{
          link_url: href,
          link_location: a.className || 'link',
          page_language: document.documentElement.lang
        }});
      }});
    </script>
    <!-- GA:END -->"""

pages = sorted(p for p in [*ROOT.glob("*.html"), *ROOT.glob("ja/*.html"), *ROOT.glob("zh-tw/*.html")]
               if not p.name.startswith("source_"))
for p in pages:
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"\s*<!-- GA:START -->.*?<!-- GA:END -->", "", s, flags=re.S)
    s, n = re.subn(r"(<head[^>]*>)", lambda m: m.group(1) + "\n    " + SNIPPET, s, count=1)
    assert n == 1, p
    p.write_text(s, encoding="utf-8")
print("GA installed:", len(pages))
