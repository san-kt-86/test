"""A tiny, dependency-free website. Run with: python3 app.py"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint


PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Little Data Garden</title>
  <style>
    :root { color-scheme: light; --ink:#20342d; --muted:#718078; --green:#47765d; --cream:#f5f5ee; }
    * { box-sizing:border-box }
    body { margin:0; background:var(--cream); color:var(--ink); font:16px/1.5 system-ui,-apple-system,sans-serif }
    main { width:min(960px,calc(100% - 36px)); margin:50px auto }
    header { display:flex; justify-content:space-between; align-items:center; gap:20px; margin-bottom:28px }
    .eyebrow { color:var(--green); font-size:12px; font-weight:750; letter-spacing:.14em; text-transform:uppercase }
    h1 { margin:5px 0 0; font-size:clamp(30px,5vw,46px); letter-spacing:-.04em; line-height:1.1 }
    .date { color:var(--muted); font-size:14px }
    .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px }
    .card { background:white; border:1px solid #e6e9e0; border-radius:18px; padding:23px; box-shadow:0 5px 20px #233b2c08 }
    .metric-label { color:var(--muted); font-size:14px }
    .metric { margin:8px 0 0; font-size:34px; font-weight:700; letter-spacing:-.04em }
    .unit { color:var(--muted); font-size:14px; font-weight:500; letter-spacing:0 }
    .chart-card { grid-column:span 2; min-height:300px }
    .chart-head { display:flex; justify-content:space-between; align-items:start }
    h2 { margin:0; font-size:19px }
    .chart-head p { margin:4px 0; color:var(--muted); font-size:13px }
    .chart { width:100%; height:205px; margin-top:14px; overflow:visible }
    .chart .area { fill:url(#wash) }
    .chart .line { fill:none; stroke:var(--green); stroke-width:3; stroke-linecap:round; stroke-linejoin:round }
    .chart .dot { fill:white; stroke:var(--green); stroke-width:3 }
    .chart .gridline { stroke:#e9eee8; stroke-width:1 }
    .side-card { display:flex; flex-direction:column; justify-content:space-between; background:#e7eee5 }
    .leaf { font-size:42px }
    .note { color:#52665a; font-size:14px }
    .refresh { margin-top:18px; padding:11px 16px; border:0; border-radius:10px; background:var(--green); color:white; font:600 14px system-ui; cursor:pointer }
    .refresh:hover { background:#365e49 }
    footer { margin-top:20px; color:var(--muted); font-size:12px; text-align:center }
    @media(max-width:650px) { main{margin:28px auto}.grid{grid-template-columns:1fr}.chart-card{grid-column:auto}.side-card{min-height:190px} }
  </style>
</head>
<body><main>
  <header><div><div class="eyebrow">A tiny snapshot</div><h1>Little Data Garden</h1></div><div class="date">A fresh batch of made-up data</div></header>
  <section class="grid">
    <article class="card"><div class="metric-label">Garden visitors</div><div class="metric">__VISITORS__ <span class="unit">today</span></div></article>
    <article class="card"><div class="metric-label">Happiness index</div><div class="metric">__HAPPY__<span class="unit"> / 100</span></div></article>
    <article class="card"><div class="metric-label">Ideas growing</div><div class="metric">__IDEAS__ <span class="unit">new sprouts</span></div></article>
    <article class="card"><div class="metric-label">Feature A</div></article>
    <article class="card chart-card">
      <div class="chart-head"><div><h2>Daily sunshine</h2><p>Imaginary hours of sunshine this week</p></div><div class="eyebrow">This week</div></div>
      <svg class="chart" viewBox="0 0 600 205" role="img" aria-label="A line chart showing sunshine hours over seven days">
        <defs><linearGradient id="wash" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#8eb89a" stop-opacity=".35"/><stop offset="1" stop-color="#8eb89a" stop-opacity="0"/></linearGradient></defs>
        <line class="gridline" x1="20" y1="35" x2="580" y2="35"/><line class="gridline" x1="20" y1="90" x2="580" y2="90"/><line class="gridline" x1="20" y1="145" x2="580" y2="145"/>
        <path class="area" d="__AREA__"/><path class="line" d="__LINE__"/>__DOTS__
        <g fill="#718078" font-size="12" text-anchor="middle"><text x="35" y="194">Mon</text><text x="123" y="194">Tue</text><text x="211" y="194">Wed</text><text x="299" y="194">Thu</text><text x="387" y="194">Fri</text><text x="475" y="194">Sat</text><text x="565" y="194">Sun</text></g>
      </svg>
    </article>
    <article class="card side-card"><div><div class="leaf">🌱</div><h2>A little reminder</h2><p class="note">Small things add up. Take a breath, stretch your legs, and let one good idea grow.</p></div><div class="eyebrow">Grown with Python</div></article>
  </section>
  <form method="get"><button class="refresh" type="submit">↻ Grow a new snapshot</button></form>
  <footer>All numbers are randomly generated for fun.</footer>
</main></body></html>"""


def make_page():
    values = [randint(2, 9) for _ in range(7)]
    points = [(35 + i * (530 / 6), 155 - value * 13) for i, value in enumerate(values)]
    line = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
    area = f"{line} L 565 170 L 35 170 Z"
    dots = "".join(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="5"/>' for x, y in points)
    return (PAGE.replace("__VISITORS__", str(randint(84, 320)))
            .replace("__HAPPY__", str(randint(72, 99)))
            .replace("__IDEAS__", str(randint(3, 18)))
            .replace("__AREA__", area).replace("__LINE__", line).replace("__DOTS__", dots))


class SiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = make_page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8080), SiteHandler)
    print("Serving Little Data Garden at http://127.0.0.1:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
        server.server_close()
