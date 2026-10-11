# Brief: TechNext industry social posts (hero-scene style)

Work folder: `C:\Users\leuss\ClaudeWork\site-posts-2026-10-08-ind` (run every command from here).
Reference post (DONE, copy its structure exactly): `v3/p04.html` (Medical) and its render `qa/p04.jpg` - LOOK at it first.

## What the owner wants
- One 3:4 image post per industry (1080x1440 CSS px, rendered 2160x2880). Images only.
- "dont use too much comical style. focus on similar style that we currently using to build hero section in all pages."
  => soft flat hero look of technext.asia: front-on pastel room (K.room wall + wainscot + floor), soft shadows,
  the pill-flat cast drawn with the site's own kit (K.person via H.who/H.person), plaques, windows, plants, light pools.
  NO ink outlines, NO hard offset "lip" shadows, NO comic stamps/stickers.
- Earlier rule: don't copy the website page - make a NEW composition per post (new room layout, new props, new
  camera framing), only the style is shared. Every post must look different from the others (layout of card,
  palette, framing, where the people stand).
- Fonts/colours: TechNext brand (Plus Jakarta Sans, Inter, Caveat kicker) - already in assets/scene.css.

## Fixed frame (keep exactly as p04)
TechNext logo top-left, Odoo wordmark top-right (`.sp-logos`), URL pill `.sp-url.soft` at the bottom
(left or right or centre - vary it), text `.card` with `.k` kicker, `h1` (with an `<em>` accent phrase), `p`, `.apps`
chips with real Odoo icons from `../assets/img/odoo/<name>.svg` (ls that folder), 1-2 `.rec` floating Odoo record
cards (each with `<small>sample</small>`). Every text block has `data-qa="..."`; the canvas has `data-qa-skip`.

## How to draw
- `<canvas id="scene">`, then `../assets/js/industry-world.js` + `../assets/scene-post.js`, then
  `SP.draw(function (g, K, H) { ... })`. Pattern from p04: `var k=1.6, sx=..., sy=...; K.room(g,1080,1440,k,sx,sy,{...});
  g.save(); g.translate(sx,sy); g.scale(k,k); /* set units: floor at y 470 */ ...; g.restore();` then
  foreground H.blur / H.pool / H.vignette in post px.
- Kit (window.IXW.kit, see `assets/js/industry-world.js` around lines 20-60, 226-420): rr, fillRR, fillE, ell, limb,
  soft, shadowed, text, tone, person, room, plusPattern, windowFrame, windowSky, windowGlass, windowMullions, cloud,
  plaque, clockFace, clockHands, plant, FONT. Person options are documented at the top of that file (outfit
  scrubs|coat|blazer|tee|hoodie, hairStyle, hat sunhat|cap|hardhat|toque, apron, vest, headset, hold
  clipboard|passport|bags|box|tablet|tray|mat, sit, glasses, mood, look, talk, hands [[lx,ly],[rx,ry]]).
  For more prop ideas read the matching site world `C:\Users\leuss\ClaudeWork\tn-social-ref\assets\js\worlds\<key>.js`
  (style reference only; write your own composition, don't paste its scene).
- Cast: Southeast-Asian / East-Asian skin tones and dark hair (target market SG/PH/VN), varied ages, glasses, builds.
  No wheelchairs. Clients/customers may wear casual clothes; staff in the industry's uniform.
- Content: industry line from the site menu, Odoo processes real, numbers and names labelled sample.
  Claims only: TechNext = Odoo Partner, SG HQ + PH + VN teams. CTA URL `technext.asia/industries/<key>`
  (keys: medical, travel, retail, ecommerce, construction, fnb, manufacturing, health-wellness).
- Script gotcha: never name a global `top`, `name`, `status` (window properties) - the drawing silently fails.

## Render + QA loop (required)
`python C:\Users\leuss\.claude\skills\technext-site-posts\scripts\render.py v3/pNN.html --out qa --force --port <yours>`
then make a jpg and LOOK at it with the Read tool:
`python -c "from PIL import Image; Image.open('qa/NN-technext-<title>.png').convert('RGB').resize((1080,1440)).save('qa/pNN.jpg',quality=85)"`
Iterate until (a) the render prints ALL CLEAN without --force, and (b) it looks right: no face covered by a card,
no prop overlapping a person awkwardly, people standing on the floor, nothing important under the URL pill or logos,
card text not over busy art. Use your own port so you don't collide with others.

## Posts
| NN | Industry | key | `<title>` | menu line |
|---|---|---|---|---|
| 04 | Medical | medical | odoo-for-medical | Clinics and healthcare groups. (DONE) |
| 05 | Travel | travel | odoo-for-travel | Agencies, tours and hospitality. |
| 06 | Retail | retail | odoo-for-retail | Stores, POS and stock in one place. |
| 07 | Ecommerce | ecommerce | odoo-for-ecommerce | Online orders, fulfilment and books. |
| 08 | Construction | construction | odoo-for-construction | Projects, site costs and progress billing. |
| 09 | F&B | fnb | odoo-for-fnb | Restaurants, cafés and central kitchens. |
| 10 | Manufacturing | manufacturing | odoo-for-manufacturing | Bills of materials, work orders, costing. |
| 11 | Health & Wellness | health-wellness | odoo-for-health-wellness | Studios, spas, memberships and retail. |

When done, reply with: file paths, the final QA line, and one sentence per post describing the composition.
Don't deliver anywhere, don't edit p04 or other agents' files.
