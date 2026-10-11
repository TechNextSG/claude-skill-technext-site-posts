"""Build one 3:4 post page from a capture (scene.png + page.json) and a small spec.

    python make_post.py specs/p01.json [...]      (run from the work folder)

The post is the site page itself, re-staged: the page's own scene, the page's own card markup and world CSS
(so the card skin, hand-lettered kicker, chips and the world's unique buttons are exactly the website's),
the page's own Nexi caption bubble, plus the fixed social frame (TechNext logo top-left, Odoo wordmark top-right,
URL footer). Work-folder layout (make it with setup.py):
    assets/        copy of the site's assets/css + assets/img (setup.py)
    cap/<k>/       scene.png + page.json (capture.py)
    posts/pNN.html written here; open with ?qa=1 to outline every text box

Spec keys (all optional except cap/out):
  cap      "cap/erp"                      capture folder
  out      "posts/p01.html"
  slug     "odoo-erp-implementation"      file slug for the render
  card     {"x":44,"y":132,"w":560,"zoom":1.2}   card box in post px (1080x1440 frame), zoom scales the site card
  hand     replaces the hand-lettered kicker;  h1  replaces the headline (keep the page's own unless asked)
  lead     replaces the lead paragraph (short, 1-2 lines; post copy, not page copy)
  keep     list of card parts to keep beyond ep/h1/lead/actions, e.g. [".orc-apps"]  (crumbs + hint always go)
  ghost    relabel the second button (default: the page's own label; the URL is already in the footer)
  cap_box  {"x":..,"y":..,"w":..}  Nexi caption bubble; omit to leave it out
  say      caption text (may contain <b>);  rec  the caption's record line (labelled Sample)
  tint     "#hex" logo-row backing tint when the top of the scene is busy (default none)
"""
import html, json, pathlib, re, sys

FRAME = """<!doctype html>
<html lang="en" class="sp-html">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&family=Caveat:wght@500;600;700&display=swap">
{sheets}
<link rel="stylesheet" href="../assets/site-post.css">
<style>
:root{{--cx:{cx}px;--cy:{cy}px;--cw:{cw}px;--cz:{cz};--cr:{cr}deg}}
{extra_css}
</style>
</head>
<body class="{body_cls} sp-post">
<div class="sp-frame" data-sp-frame>
  <div class="sp-cam"><img class="sp-scene" src="../{scene}" alt="" style="{scene_style}"></div>
  {fx}
  <div class="sp-logos"{tint}>
    <img class="sp-tn" src="../assets/img/logo-horizontal.png" alt="TechNext">
    <img class="sp-odoo" src="../assets/sp/odoo-logo.png" alt="Odoo">
  </div>
  <main id="main"><section class="ixw-hero is-live"><div class="container ixw-hero-in">
    <div class="sp-card">{copy}</div>
  </div></section>
  {cap}
  </main>
  {fx_top}
  <div class="sp-foot"><span class="sp-url">{url}</span></div>
</div>
</body>
</html>
"""


def strip(markup, sel_tag, cls):
    """Remove the first element <sel_tag class="...cls..."> ... </sel_tag> (non-nested tags only)."""
    return re.sub(r'<%s class="[^"]*\b%s\b[^"]*"[^>]*>.*?</%s>' % (sel_tag, re.escape(cls), sel_tag), "", markup, count=1, flags=re.S)


def build(spec_path):
    spec_path = pathlib.Path(spec_path)
    root = pathlib.Path.cwd()   # run from the work folder
    s = json.loads(spec_path.read_text(encoding="utf-8"))
    cap_dir = root / s["cap"]
    pg = json.loads((cap_dir / "page.json").read_text(encoding="utf-8"))
    url = pg["url"].split("//", 1)[1]
    url = re.sub(r"^(127\.0\.0\.1|localhost)(:\d+)?", "technext.asia", url).replace("www.", "")
    copy = pg["copy"]
    copy = strip(copy, "nav", "crumbs")
    copy = strip(copy, "p", "ixw-hint")
    for part in ("orc-apps", "twr-tags"):
        if "." + part not in s.get("keep", []):
            copy = re.sub(r'<div class="%s">.*?</div>(?=\s*<div class="actions")' % part, "", copy, flags=re.S)
    if s.get("hand"):
        copy = re.sub(r'(<span class="hand h1-hand">).*?(</span>)', r"\g<1>%s\2" % s["hand"], copy, count=1, flags=re.S)
    if s.get("h1"):
        copy = re.sub(r'(<span class="sr-only">[^<]*</span>).*?(</h1>)', r"\g<1>%s\2" % s["h1"], copy, count=1, flags=re.S)
    if "lead" in s and not s["lead"]:
        copy = re.sub(r'<p class="lead">.*?</p>', "", copy, count=1, flags=re.S)
    elif s.get("lead"):
        copy = re.sub(r'<p class="lead">.*?</p>', '<p class="lead">%s</p>' % s["lead"], copy, count=1, flags=re.S)
    ghost = s.get("ghost")
    if ghost: copy = re.sub(r'(<a class="btn btn-ghost[^"]*"[^>]*>)(.*?)(</a>)',
                  lambda m: m.group(1) + re.sub(r"[^<>]+$", "", m.group(2)) + html.escape(ghost) + m.group(3), copy, count=1, flags=re.S)
    cap = ""
    if s.get("cap_box") and pg.get("cap"):
        cap = pg["cap"]
        cap = re.sub(r'<div class="ixw-cap-side">.*$', "</div>", cap, flags=re.S)   # controls go; close the cap
        cap = re.sub(r'\bis-typing\b', "", cap)
        cap = re.sub(r'(<span data-ixw-type="">).*?(</span>)', r"\g<1>%s\2" % s.get("say", ""), cap, count=1, flags=re.S)
        cap = cap.replace('<i class="ixw-caret"></i>', "")
        rec = s.get("rec")
        cap = re.sub(r'<p class="ixw-cap-rec"[^>]*>.*?</p>',
                     ('<p class="ixw-cap-rec"><span>%s</span><em>Sample</em></p>' % rec) if rec else "", cap, count=1, flags=re.S)
        cap = cap.replace('style="translate: 0px;"', "")
        b = s["cap_box"]
        cap = '<div class="sp-cap" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (b["x"], b["y"], b["w"], cap)
    sheets = []
    for href in pg["sheets"]:
        if "fonts.googleapis" in href:
            continue
        p = re.sub(r"^https?://[^/]+/", "../", href).split("?")[0]
        sheets.append('<link rel="stylesheet" href="%s">' % p)
    body_cls = pg["chain"][0]["cls"].replace("tabs-wait", "").strip()
    c = dict({"x": 44, "y": 132, "w": 560, "zoom": 1.2, "rot": 0}, **s.get("card", {}))
    sc = s.get("scene", {})
    scene_src = f'{s["cap"]}/{sc.get("src", "scene.png")}'
    if sc:
        from PIL import Image
        iw, ih = Image.open(cap_dir / sc.get("src", "scene.png")).size
        k = sc.get("s", 1) * sc.get("css_w", 1600) / iw          # post px per image px
        scene_style = ("width:%.1fpx;height:%.1fpx;left:%.1fpx;top:%.1fpx;transform-origin:%s;transform:rotate(%sdeg)"
                       % (iw * k, ih * k, sc.get("x", 0), sc.get("y", 0), sc.get("origin", "540px 720px"), sc.get("rot", 0)))
    else:
        scene_style = "width:1080px;height:1440px;left:0;top:0"
    out = root / s["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(FRAME.format(
        title=html.escape(s.get("slug", out.stem)), sheets="\n".join(sheets), cx=c["x"], cy=c["y"], cw=c["w"], cz=c["zoom"], cr=c["rot"], scene_style=scene_style, fx=s.get("fx", ""), fx_top=s.get("fx_top", ""),
        extra_css=s.get("css", ""), body_cls=body_cls, scene=scene_src,
        tint=(' style="--sp-tint:%s"' % s["tint"]) if s.get("tint") else "",
        copy=copy, cap=cap, url=html.escape(url)), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        build(a)
