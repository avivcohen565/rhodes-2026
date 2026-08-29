#!/usr/bin/env python3
"""בונה את index.html (גרסת הנייד) מתוך src/page.html.
הרצה:  python3 build.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "src" / "page.html").read_text(encoding="utf-8")

style = re.search(r"<style>.*?</style>", src, re.S).group(0)
body = src[src.index('<div class="wrap">'):]

IDS = {
    "מה כבר סגור": "bookings",
    "הכל על ציר אחד": "map",
    "בוקר": "morning",
    "צהריים": "noon",
    "ערב": "evening",
    "איך זה מתחלק על 5 הימים": "plan",
    "כל המקומות שנאספו": "index",
    "מה כדאי לסגור עכשיו, ומה כדאי לדעת": "notes",
}
NAV = [("bookings", "הזמנות"), ("map", "מפה"), ("morning", "בוקר"),
       ("noon", "צהריים"), ("evening", "ערב"), ("plan", "5 ימים"),
       ("index", "כל המקומות"), ("notes", "הערות")]


def add_id(m):
    tag, inner = m.group(1), m.group(2)
    h2 = re.search(r"<h2>(.*?)</h2>", inner, re.S)
    if h2 and h2.group(1).strip() in IDS:
        return tag[:-1] + ' id="%s">' % IDS[h2.group(1).strip()] + inner
    return m.group(0)


body = re.sub(r"(<section[^>]*>)(.*?</section>)", add_id, body, flags=re.S)

nav = '<nav class="qnav" aria-label="ניווט מהיר">\n' + "".join(
    '  <a href="#%s">%s</a>\n' % (i, label) for i, label in NAV) + "</nav>\n"
body = body.replace("</header>", "</header>\n" + nav, 1)

MOBILE_CSS = """<style>
/* ---------- mobile shell ---------- */
html{scroll-behavior:smooth}
body{-webkit-tap-highlight-color:transparent;overflow-x:hidden}
.qnav{
  position:sticky;top:0;z-index:50;
  display:flex;gap:6px;overflow-x:auto;
  margin:0 -20px 34px;padding:10px 20px;
  background:color-mix(in srgb, var(--ground) 88%, transparent);
  backdrop-filter:saturate(150%) blur(12px);
  -webkit-backdrop-filter:saturate(150%) blur(12px);
  border-bottom:1px solid var(--line);
  scrollbar-width:none;
}
.qnav::-webkit-scrollbar{display:none}
.qnav a{
  flex:none;
  font-family:"Heebo",sans-serif;font-size:13px;font-weight:500;
  color:var(--ink-2);text-decoration:none;
  padding:7px 13px;border-radius:999px;
  border:1px solid var(--line);
  background:var(--surface);
  white-space:nowrap;
}
.qnav a:hover,.qnav a:focus-visible{color:var(--accent);border-color:var(--accent)}
section[id]{scroll-margin-top:64px}
.mapwrap{-webkit-overflow-scrolling:touch}
@media (max-width:640px){
  body{font-size:16px}
  .wrap{padding:0 16px 72px}
  header{padding:34px 0 22px;margin-bottom:26px}
  .qnav{margin:0 -16px 26px;padding:10px 16px}
  .card{padding:17px 17px 15px}
  .notes{padding:18px 18px}
  .mapwrap::after{
    content:"↔ אפשר לגרור את המפה הצידה";
    display:block;padding:8px 12px;font-family:"Heebo",sans-serif;
    font-size:12px;color:var(--muted);background:var(--surface-2);
    border-top:1px solid var(--line);position:sticky;left:0;
  }
}
@media print{.qnav{display:none}body{background:#fff;color:#000}}
</style>"""

HEAD = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>רודוס לפי שעות היום</title>
<meta name="description" content="כל המקומות ברודוס מקישורי הטיקטוק של הקבוצה, לפי בוקר / צהריים / ערב, עם מחירים ומרחקים מהמלון.">
<meta name="theme-color" content="#EFF2F0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1615" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="רודוס">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8F%9B%EF%B8%8F%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&family=Frank+Ruhl+Libre:wght@500;700;900&family=Heebo:wght@400;500;700&display=swap">
"""

doc = HEAD + style + "\n" + MOBILE_CSS + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"
(ROOT / "index.html").write_text(doc, encoding="utf-8")
print("index.html נכתב —", len(doc), "בתים")
