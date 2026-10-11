"""Capture a technext.asia page's own hero scene as a 3:4 post background, plus the page's card + caption markup.

    python capture.py <page path> <out dir> [--base URL] [--x0 400] [--h 1600] [--dpr 1.8] [--wait 4]

<page path> e.g. solutions/odoo-erp. The page is opened at 1600 css px wide (desktop layout) with the hero
stretched to --h px, so the world paints its own extended sky/wall above the scene (scenes are bottom-anchored
and scale by width). Overlays (header, side tabs, card, caption, peek/drag, hot labels, cookie banner) are
hidden; the touring Nexi stays. The 1200 x h strip starting at --x0 is saved:
  <out>/scene.png    2160 x 2880 at the defaults (1200*1.8 x 1600*1.8)
  <out>/page.json    {url, title, chain, copy, cap, sheets, vars}  - the page's own card/caption HTML,
                     the ancestor class chain (world skins are scoped to it) and its stylesheet URLs
"""
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cdp
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ap = argparse.ArgumentParser()
ap.add_argument("page"); ap.add_argument("out")
ap.add_argument("--base", default="http://127.0.0.1:4011")
ap.add_argument("--x0", type=int, default=400)
ap.add_argument("--w", type=int, default=1200)
ap.add_argument("--h", type=int, default=1600)
ap.add_argument("--dpr", type=float, default=1.8)
ap.add_argument("--wait", type=float, default=4.0)
ap.add_argument("--port", type=int, default=9871)
ap.add_argument("--name", default="scene.png")
a = ap.parse_args()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
url = f"{a.base.rstrip('/')}/{a.page.strip('/')}?nointro=1&nc={int(time.time()) % 99999}"

HIDE = ("header,.side-tabs,.side-fab,.ixw-copy,.ixw-cap,.ixw-peek,.ixw-drag,.ixw-hot-lab,#tn-cookie-banner,"
        ".ixw-credits-wrap,.skip-link{visibility:hidden!important;opacity:0!important}"
        ".ixw-hero{height:%dpx!important;min-height:%dpx!important;max-height:none!important}" % (a.h, a.h))

GRAB = r"""(function(){
  var copy=document.querySelector('.ixw-copy'), cap=document.querySelector('.ixw-cap');
  var chain=[], n=copy;
  while(n && n!==document.documentElement){ chain.unshift({tag:n.tagName.toLowerCase(), cls:n.className||'', id:n.id||'', style:n.getAttribute('style')||''}); n=n.parentElement; }
  chain.pop();  // the card itself
  var sheets=[].slice.call(document.querySelectorAll('link[rel=stylesheet]')).map(function(l){return l.href});
  return {url:location.href.split('?')[0], title:document.title, chain:chain,
          copy:copy?copy.outerHTML:'', cap:cap?cap.outerHTML:'', sheets:sheets,
          html:document.documentElement.className, body:document.body.className};
})()"""

proc, c = cdp.session(a.port)
try:
    c.metrics(1600, 900)
    c.go(url, 2.0)
    info = c.ev(GRAB)
    c.metrics(1600, a.h, a.dpr)
    c.ev("(function(){var s=document.createElement('style');s.textContent=%s;document.head.appendChild(s);"
         "window.scrollTo(0,0);window.dispatchEvent(new Event('resize'))})()" % json.dumps(HIDE))
    time.sleep(a.wait)
    top = c.ev("document.querySelector('.ixw-hero').getBoundingClientRect().top")
    c.shot(out / a.name, {"x": a.x0, "y": max(0, top), "width": a.w, "height": a.h})
    (out / "page.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print("saved", out / a.name, "and page.json  (", info["title"], ")")
finally:
    proc.terminate()
